from typing import List, Any

import redis
from redis_lru import RedisLRU

from models import Author, Quote

client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)


@cache
def find_by_tag(tag: str) -> list[str | None]:
    print(f"Find by {tag}")
    quotes = Quote.objects(tags__iregex=tag)
    result = [q.quote for q in quotes]
    return result


@cache
def find_by_tags(req: str) -> list[str | None]:
    print(req)
    tags = [tag.strip() for tag in req.split(":")[1].split(",")] 
    print(f"Find by {tags}")
    quotes = Quote.objects(tags__in=tags)
    result = [q.quote for q in quotes]
    return result


@cache
def find_by_author(author: str) -> list[list[Any]]:
    print(f"Find by {author}")
    authors = Author.objects(fullname__iregex=author)
    result = {}
    for a in authors:
        quotes = Quote.objects(author=a)
        result[a.fullname] = [q.quote for q in quotes]
    return result


def request_search(comm: str):
    if comm.startswith('name'):
        author_name = comm.split(":")[1].strip()
        print(find_by_author(author_name))
    elif comm.startswith('tags'):
        print(find_by_tags(comm))
    elif comm.startswith('tag'):
        tag = comm.split(":")[1].strip()
        print(find_by_tag(tag))

        

if __name__ == '__main__':
    while True:
        request = input("Enter the request: ")
        request_search(request)
        if request.lower() == "exit":
            break
    # print(find_by_tag('mi'))
    # print(find_by_tag('mi'))

    # print(find_by_author('in'))
    # print(find_by_author('in'))

    # print(find_by_tags("tags:life,live"))
    # print(find_by_tags("tags:life,live"))
    # # quotes = Quote.objects().all()
    # # print([e.to_json() for e in quotes])

