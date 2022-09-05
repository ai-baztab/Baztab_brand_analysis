import numpy as np
import pandas as pd

class Media:
    def __init__(self, id, url, date, like_view=0, caption="None", tags = None):
        self.media_url = url
        self.caption = caption
        self.date = date
        self.tags = tags
        self.comments = []
        self.likes_views = like_view
        self.id = id # most important

