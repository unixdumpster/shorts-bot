def split_content(reddit_post, words_per_subtext):
    title = reddit_post.title
    original_text = reddit_post.selftext

    words = original_text.split()

    result = []
    story_part = 1
    # 10 words is threshold in which I think is an ok place to not post the video just because there's no content left.
    while len(words) > 10:
        # print(result)
        result.append((f"part {str(story_part)}, {title}. ", ' '.join(words[:words_per_subtext])))
        words = words[words_per_subtext:]
        story_part += 1
    return result

def proofread(text):
    result = text.replace("AITAH", "Am I the ayy whole").replace("AITA", "Am I the ayy whole").replace("TIFU", "Today I fudged up").replace("Aita", "Am I the ayy whole").replace("fuck", "fudge")
    return result