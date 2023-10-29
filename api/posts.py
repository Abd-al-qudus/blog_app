"""
    This module handles the user post and comments
    """

from .database import DATABASE
from .models import BlogPost, Comment


class POSTS:
    """handle user posts"""
    
    def __init__(self) -> None:
        self._session = DATABASE()._session
    
    def get_all_posts(self) -> BlogPost:
        """get all user post"""
        posts = self._session.query(BlogPost).all()
        return posts
    
    def get_posts_by_id(self, id: int) -> BlogPost:
        """fetch post by id"""
        try:
            post = self._session.query(BlogPost).filter_by(id=id).first()
            return post
        except Exception as e:
            print(f"Error in get_posts_by_id: {str(e)}")
            return None
    
    def delete_postById(self, id: int)-> bool:
        """delete post by id"""
        post_to_delete = self.__session.query(BlogPost).get(id)
        try:
            self.__session.delete(post_to_delete)
            self.__session.commit()
            return True
        except:
            return False
        
    def get_all_comments(self, post_id: int) -> Comment:
        """get comments on post"""
        return self._session.query(Comment).filter_by(post_id=post_id).all()
    
    def add_newComments(self, text:str, comment_author:str, parent_post: int ) -> Comment:
        """add new comment on a post"""
        new_comment = Comment()
        self._session.add(new_comment)
        self._session.commit()
        return new_comment
