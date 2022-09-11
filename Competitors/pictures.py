import numpy as np
import pandas as pd

class Media:
    def __init__(self, media_id, url, i_or_v, detail, like_view):
        self.media_url = url
        self.type = i_or_v
        post_info = detail[0]
        self.caption = post_info[1]
        self.date = post_info[2]
        # the tags are mostly in a comment
        # add a function to extract tags from caption or the other comment
        # self.tags = tags
        try:
            self.comments = detail[1, :]
        except:
            self.comments = []
        self.likes_views = like_view
        self.id = media_id

    def extract_tags(self):
        pass

