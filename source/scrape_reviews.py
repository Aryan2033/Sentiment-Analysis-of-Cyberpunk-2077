import requests
import pandas as pd
import time
import urllib.parse

def get_steam_reviews(app_id, target_count=100000):
    reviews = []
    cursor = '*'
    
    while len(reviews) < target_count:
        # Steam API requires cursor to be URL encoded
        url = f"https://store.steampowered.com/appreviews/{app_id}?json=1&filter=recent&language=english&review_type=all&purchase_type=all&num_per_page=100&cursor={urllib.parse.quote(cursor)}"
        
        try:
            response = requests.get(url, timeout=10)
        except requests.exceptions.RequestException as e:
            print(f"Network error: {e}")
            break
            
        if response.status_code != 200:
            print(f"Failed to fetch data. Status code: {response.status_code}")
            break
            
        data = response.json()
        
        if data.get('success') != 1:
            print("API returned unsuccessful response.")
            break
            
        batch_reviews = data.get('reviews', [])
        
        if not batch_reviews:
            print("No more reviews found.")
            break
            
        for review in batch_reviews:
            reviews.append({
                'review_text': review.get('review'),
                'voted_up': review.get('voted_up'),  # True = Positive, False = Negative
                'votes_up': review.get('votes_up'),  # How many other users found this review helpful
                'playtime_forever': review.get('author', {}).get('playtime_forever'),
                'timestamp_created': review.get('timestamp_created') # Added for Time-Series!
            })
            
            if len(reviews) >= target_count:
                break
                
        # Update cursor for the next batch
        new_cursor = data.get('cursor')
        if not new_cursor or new_cursor == cursor:
            break
        cursor = new_cursor
        
        print(f"Collected {len(reviews)} reviews so far...")
        # Pause for 0.5 seconds between requests so we don't overload the Steam server and get blocked
        time.sleep(0.5) 
        
    return reviews

if __name__ == "__main__":
    # 1091500 is the App ID for Cyberpunk 2077. You can change this to any game ID.
    # Other examples: 413150 (Stardew Valley), 1245620 (Elden Ring)
    app_id = "1091500" 
    target = 100000
    
    print(f"Starting to scrape {target} reviews...")
    reviews_data = get_steam_reviews(app_id, target_count=target)
    
    df = pd.DataFrame(reviews_data)
    
    # Drop any rows where the review text might be empty
    df = df.dropna(subset=['review_text'])
    
    # Save the dataset to CSV
    output_file = "steam_reviews_dataset.csv"
    df.to_csv(output_file, index=False)
    print(f"\nSUCCESS! Saved {len(df)} reviews to {output_file}")
