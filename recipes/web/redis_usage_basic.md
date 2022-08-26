# Redis Basic Usage

## Core Data Types

- String
- List
- Set
- Hash
- Sorted Set

## Basic Usage

```bash
redis-cli

> select <db-index>  # 0-16 by default
```

## Key

```bash
# Key
#
# - Very long keys are not a good idea.
# - The maximum allowed key size is 512 MB.
# - Try to stick with a schema: 'user:001:reply-to'
# - The empty string is also a valid key.
> exists <key>  # return 0 or 1
> del <key>  # return 0 or 1
> type <key>  # return none, string or ...
> keys *  # be careful!


# Key expiration
#
# - also known as a "time to live", or "TTL".
# - both using seconds or milliseconds precision.
# - the expire time resolution is always 1 millisecond.
# - Information about expires are replicated and persisted on disk,
#   the time virtually passes when your Redis server remains stopped
#   (this means that Redis saves the date at which a key will expire).
> expire <key> <seconds-int>
> pexpire <key> <milliseconds-int>
> persist <key>  # persistent forever
> ttl <key>  # return the remaining time to live in seconds
> pttl <key>  # return the remaining time to live in milliseconds
```

## String

```bash
# String
> set <key> <value>
> set <key> <value> ex <expire-seconds-int>
> set <key> <value> px <expire-milliseconds-int>
> get <key>

> incr <key>  # atomic
> decr <key>  # atomic
> incrby <key> <value>  # atomic, return result
> decrby <key> <value>  # atomic, return result

> getset <key> <value>  # set new value, get old value

> mget <k1> <k2> ...  # return an array of values
> mset <k1> <v1> <k2> <v2> ...
```

## List

```bash
# List
#
# - Redis lists are implemented via Linked Lists.
# - This means that even if you have millions of elements inside a list,
#   the operation of adding a new element in the head or in the tail of the list
#   is performed in *constant time* (`O(1)`).
# - What's the downside?
#   Accessing an element by index is very fast in lists implemented with an Array (constant time indexed access)
#   and not so fast in lists implemented by linked lists.
#   In this case, use Sorted Set instead.
> rpush <key> <item> ...  # push on the right (tail), return count of items
> lpush <key> <item> ...  # push on the left (head), return count of items

# performs an O(N) operation
> lrange <key> <start-index> <end-index>
> rrange <key> <start-index> <end-index>

# pop elements
> rpop <key>  # right
> lpop <key>  # left
> rpop <key>  # return NULL if no item exists
(nil)

# Blocking
#
# - 0 as timeout to wait for elements forever
# - If the timeout is reached, NULL is returned.
> brpop <key> <timeout-seconds>
> blpop <key> <timeout-seconds>

# trim
#
# All the elements outside the given range are removed/discarded.
> ltrim <key> <start-index> <end-index>
> rtrim <key> <start-index> <end-index>

> llen <key>
```

## Hash

```python
> hset <key> <f1> <v1> <f2> <v2> ...
> hget <key> <f1>
> mhget <key> <f1> <f2> ...  # return an array of values

> hincrby <key> <field> <value>  # return result
> hdecrby <key> <field> <value>  # return result
```

## Set

```python
> sadd <key> <v1> <v2> ...  # return number of elements added
> sismember <key> <value>  # return 0 or 1
> smembers <key>  # return all elements
> scard <key>  # return number of all elements

> sinter <k1> <k2> ...  # intersection
> sunionstore <k1> <k2> ...  # union

> spop <key>  # pop a random element
> srandmember  # return (not remove) a random element
```

## Sorted Set

```python
# Sorted Set
#
# They are ordered according to the following rule:
#
#   - If B and A are two elements with a different score,
#     then A > B if A.score is > B.score.
#   - If B and A have exactly the same score,
#     then A > B if the A string is lexicographically greater than the B string.
#     B and A strings can't be equal since sorted sets only have unique elements.
> zadd <key> <score1> <string-element1> ...

# performs an O(log(N)) operation
# score could be `-inf` and `inf`
> zrange <key> <start-score> <end-score> [withscores]
> zrevrange <key> <start-score> <end-score> [withscores]  # reverse range
> zrangebyscore <key> <start-score> <end-score>
> zremrangebyscore <key> <start-score> <end-score>  # remove elelements whose score range from ... to ...
> zrangebylex <key> [<start-letter> [<end-letter>

> zrank <key> <string-element>  # position
> zrevrank <key> <string-element>  # reverse position
```

## Bitmap

```bash
# Bitmap
#
# Bitmaps are not an actual data type, but a set of bit-oriented operations defined on the String type.
# Since strings are binary safe blobs and their maximum length is 512 MB,
# they are suitable to set up to 2^32 different bits.
#
# One of the biggest advantages of bitmaps is that they often provide extreme space savings when storing information.
#
# Common use cases for bitmaps are:
#
# - Real time analytics of all kinds.
# - Storing space efficient but high performance boolean information associated with object IDs.
> setbit <key> <position> <0 or 1>
> getbit <key> <position>
> bitcount <key>  # report the number of bits set to 1.
```

## References

- [Redis Documentation](https://redis.io/docs/)
