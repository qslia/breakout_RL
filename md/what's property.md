what is @property
---
`@property` is a Python **decorator** that lets you define a method that can be accessed like an **attribute** (without parentheses).

## Basic Idea

Normally, you'd write a method and call it with `()`:

```python
class Brick:
    def get_color(self):
        return (255, 50, 120)

brick = Brick()
print(brick.get_color())   # method call — needs ()
```

With `@property`, you call it like a variable — **no parentheses**:

```python
class Brick:
    @property
    def color(self):
        return (255, 50, 120)

brick = Brick()
print(brick.color)         # looks like an attribute — no ()
```

Both do the same thing, but `@property` gives a **cleaner, more natural syntax**.

## Why It's Useful

### 1. Read-only computed values

In the game, `special` is stored as a normal attribute, but `color` and `points` are **derived** from `row` and `col`. Instead of storing them (which wastes memory and risks getting out of sync), we compute them on the fly:

```python
class Brick:
    def __init__(self, row, col, rect):
        self.row = row
        self.col = col
        self.rect = rect
        self.special = (row % 2 == 0 and col % 2 == 0)

    @property
    def color(self):
        return NEON_PINK if self.special else NEON_GREEN

    @property
    def points(self):
        return POINTS_SPECIAL if self.special else POINTS_NORMAL
```

Now `brick.color` always reflects the current state of `brick.special`. There's **no way** for them to disagree — unlike if you had set `self.color = ...` in `__init__` and later changed `special`.

### 2. You can't accidentally overwrite them

```python
brick.color = (0, 0, 0)   # ❌ AttributeError: can't set attribute
```

`@property` without a setter is **read-only**. This protects computed values from being clobbered.

### 3. Nicer syntax in the game loop

Compare:

```python
# With @property
pygame.draw.rect(surface, brick.color, brick.rect)
self.score += brick.points

# Without @property (method version)
pygame.draw.rect(surface, brick.get_color(), brick.rect)
self.score += brick.get_points()
```

The first reads like you're accessing data. The second looks like you're asking the object to do something.

## The Full Pattern (getter + setter)

You can also define a setter if you *do* want it writable:

```python
class Player:
    def __init__(self):
        self._score = 0

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        if value < 0:
            raise ValueError("Score can't be negative")
        self._score = value

p = Player()
p.score = 50      # calls the setter (validates!)
p.score = -1      # raises ValueError
print(p.score)    # 50
```

This is how you add **validation** or **side effects** while keeping the clean `p.score = 50` syntax.

## Summary

| | Method | `@property` |
|---|---|---|
| Call syntax | `obj.method()` | `obj.attr` |
| Read-only by default | ❌ | ✅ |
| Can add validation | ✅ | ✅ (with setter) |
| Looks like data | ❌ | ✅ |

In the Breakout code, `@property` is used purely for **read-only, computed attributes** — `color` and `points` are always derived from `special`, so they should never be stored or assigned directly. `@property` enforces that.