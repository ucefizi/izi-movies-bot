class Movie:

    id: int
    name: str
    index: int
    server_id: int
    watched: bool
    username: str
    upvotes: int
    downvotes: int

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
