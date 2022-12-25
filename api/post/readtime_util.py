class PostReadTimeEngine:

    def __init__(self, post):
        self.post = post
        self.words_per_minute = 250

    def get_title(self):
        return self.post.title

    def get_tags(self):
        tag_words = []
        [tag_words.extend(tag_word.split()) for tag_word in self.post.list_of_tags]
        return tag_words

    def get_body(self):
        return self.post.body

    def get_description(self):
        return self.post.description

    def get_post_details(self):
        details = []
        details.extend(self.get_title().split())
        details.extend(self.get_body().split())
        details.extend(self.get_description().split())
        details.extend(self.get_tags())
        return details

    def get_read_time(self):
        word_length = len(self.get_post_details())
        read_time = 0
        if word_length:
            time_to_read = word_length / self.words_per_minute
            if time_to_read < 1:
                read_time = (str(round(time_to_read*60))+" seconds")
            else:
                read_time = (str(round(time_to_read))+" minutes")
            return read_time