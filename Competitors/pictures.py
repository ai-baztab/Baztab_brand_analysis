import numpy as np
import pandas as pd


class Media:
    def __init__(self, media_id, url, i_or_v, detail, like_view, p_id):
        self.media_url = url  # tick
        self.type = i_or_v  # tick
        post_info = detail[0]
        self.caption = post_info[1]  # tick
        self.date = post_info[2]  # tick
        # the tags are mostly in a comment
        # add a function to extract tags from caption or the other comment
        self.tags = []
        self.account_activity = []
        try:
            self.comments = detail[1:]
        except:
            self.comments = []
        self.likes_views = np.int(like_view.replace(',', ''))
        self.id = media_id
        self.process_comments(p_id)

    def process_comments(self, p_id):
        del_id = []
        if len(self.comments) != 0:
            for i, c in enumerate(self.comments):
                if p_id == c[0]:
                    self.account_activity.append(c)
                    del_id.extend(i)
                if '#' in c[1]:
                    # find hashtags has been used for a picture
                    worded_comment = c[1].split(' ')
                    curr_tag = [tag for tag in worded_comment if '#' in tag]
                    # check if tags have been used consequently
                    for j, t in enumerate(curr_tag):
                        if t.count('#') > 1:
                            extracted = t.split('#')
                            curr_tag[j] = extracted[1]
                            curr_tag.extend(extracted[2:])
                        else:
                            curr_tag[j] = t.replace('#', '')
                    self.tags.extend(curr_tag)
        self.comments = [self.comments[k] for k in range(len(self.comments)) if k not in del_id]

    def pic_into_row(self, col):
        # 'pic_id', 'pic_url', 'number_of_comments', 'like/view', 'caption', 'date' : this is what we expect
        return pd.DataFrame([self.id, self.media_url, len(self.comments), self.likes_views, self.caption, self.date] \
                            , columns=col)

    def comment_into_row(self, col):
        # pic_id,user,comment
        comments = np.reshape([None, None, None] * len(self.comments), (len(self.comments), 3))
        comments[:, 1:] = self.comments
        comments[:, 0] = self.id
        return pd.DataFrame(comments, columns=col)

    def tags_into_row(self, col):
        tags = np.reshape([None, None] * len(self.comments), (len(self.comments), 2))
        tags[:, 0] = self.id
        tags[:, 1] = self.tags
        return pd.DataFrame(tags, columns=col)
