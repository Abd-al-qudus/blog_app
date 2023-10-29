"""
    This module handles the user post and comments
    """

from .database import DATABASE
from .models import BlogPost, Comment, User
from sqlalchemy.exc import IntegrityError

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
    
    def delete_postById(self, post_id: int)-> bool:
        """delete post by id"""
        post_to_delete = self.get_posts_by_id(id=post_id)
        try:
            self._session.delete(post_to_delete)
            self._session.commit()
            return True
        except:
            return False
        
    def get_all_comments(self, post_id: int) -> Comment:
        """get comments on post"""
        return self._session.query(Comment).filter_by(post_id=post_id).all()
    
    def add_newPost(self, title: str, subtitle: str, body: str, img_url: str, author: str, date: str) -> BlogPost:
        """Add a new post"""
        auth = self._session.query(User).filter_by(full_name=author).first()
        newPost = BlogPost(title=title, 
                           subtitle=subtitle, body=body, 
                           img_url=img_url, 
                           author=auth, 
                           date=date)
        try:
            self._session.add(newPost)
            self._session.commit()
        except IntegrityError:
            self._session.rollback()
        return newPost
    
    def add_newComments(self, text:str, comment_author:str, parent_post: int ) -> Comment:
        """add new comment on a post"""
        auth = self._session.query(User).filter_by(email=comment_author).first()
        print(auth)
        print(auth.id)
        new_comment = Comment(text=text, comment_author=auth, parent_post=parent_post, author_id=auth.id)
        try:
            self._session.add(new_comment)
            self._session.commit()
        except IntegrityError as e:
            self._session.rollback()
            raise e
        return new_comment
    
    def edit_post(self):
        self._session.commit()
        return True
