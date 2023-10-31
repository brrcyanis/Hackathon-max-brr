---
jupyter:
  jupytext:
    cell_metadata_filter: all,-hidden,-heading_collapsed,-run_control,-trusted
    notebook_metadata_filter: all, -jupytext.text_representation.jupytext_version,
      -jupytext.text_representation.format_version,-language_info.version, -language_info.codemirror_mode.version,
      -language_info.codemirror_mode,-language_info.file_extension, -language_info.mimetype,
      -toc, -rise, -version
    text_representation:
      extension: .md
      format_name: markdown
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
  language_info:
    name: python
    nbconvert_exporter: python
    pygments_lexer: ipython3
---

Licence CC BY-NC-ND, Thierry Parmentelat


# pentominoes and exact cover

in order to work on this exercise from your laptop, {download}`start with downloading the zip<./ARTEFACTS-pentominos.zip>`

(images courtesy of wikipedia)


## exact cover

### an example 

in a nutshell, the exact cover problem is a standard, very basic mathematical problem; let's start with an example  
you feed the algorithm with a set of vectors that all have the same length, and contain 0 and 1, like e.g.

```
0:  (1 0 0 1 1 0 1 0)
1:  (1 0 0 0 1 1 0 1)
2:  (1 0 0 0 1 1 1 0)
3:  (1 0 1 0 1 1 0 0)
4:  (1 0 0 0 1 0 1 1)
5:  (1 0 1 1 1 0 0 0)
6:  (1 0 0 0 0 1 1 1)
7:  (0 1 0 1 1 0 1 0)
8:  (0 1 0 0 1 1 0 1)
9:  (0 1 0 0 1 1 1 0)
10: (0 1 1 0 1 1 0 0)
11: (0 1 0 0 1 0 1 1)
12: (0 1 1 1 1 0 0 0)
13: (0 1 0 0 0 1 1 1)
```

and the output is a subset of the input vectors, such that **each column of the input is covered exactly once**  
(of course there is the accessory question about whether there are several
solutions, but let's not dwelve into that, for now at least..)
so in the above example, there would be 2 solutions, namely

```
5:  (1 0 1 1 1 0 0 0)
13: (0 1 0 0 0 1 1 1)
```
and
```
6:  (1 0 0 0 0 1 1 1)
12: (0 1 1 1 1 0 0 0)
```


### the algorithm and its implementation in Python

this algorithm has been the subject of a famous article by Donald Knuth - one of
the fathers of Computer Science - in 2000, and is known as Knuth's Algorithm X

we're not going to go into the details of the algorithm either, but rather focus
on the application to solving pentominoes (see next section)

let us just remember that

- Algorithm X, also known as dancing links, is an extremely efficient
  implementation for solving the exact cover problem
- and fortunately for us, there is a Python implementation of it, in the `exact_cover` package

So your first task is to search for that package, install it, and read the basics about how to use it

````{admonition} Important tip !
:class: danger

during my own attempt at this exercise, I ran into a nasty bug in this library  
that was stubbornly returning 'no solution' whereas there obviously was one..

in order to work around that, I simply had to save and reload my numpy array before
I fed it into `get_exact_cover()`, like so:
```python
def workaround_sanitize(array):
    """
    save and reload to work around a sneaky bug
    in exact_cover
    """
    filename = ".sanitizing-array.txt"
    exact_cover.io.save_problem(filename, array)
    return exact_cover.io.load_problem(filename)
```
````


## application to pentominoes

### the pentominoes

and now for something completely different...  
the pentaminoes are the 12 patterns that can be made of 5 contiguous squares - modulo rotations and symmetry  
they have been given names, letters actually:

```{image} media/pentominos.png
:width: 60%
:align: center
```


### some standard problems

they can be taken as the pieces of a puzzle, and so the standard problems are to fill shapes - that must have an area of $12 * 5 = 60$ - with these 12 pieces (here again a given piece may be rotated or reversed in any position)

we'll consider here the following shapes

```{image} media/boards.png
:align: center
:width: 60%
```

as well as this one within a 8x8 square

```{image} media/board-8x8.png
:width: 40%
:align: center
```


### how to solve such a problem

the trick is to transform the puzzle problem into an exact cover problem  
there are many resources on the Internet that explain how to do that - and feel free to use them  
on our end, let's consider a smaller problem as depicted below

#### our small example

```{image} media/small-problem.png
:width: 150px
:align: center
```

it turns out this problem can be mapped to the sample input quoted above, i.e.

```
0:  (1 0   0 1 1 0 1 0)
1:  (1 0   0 0 1 1 0 1)
2:  (1 0   0 0 1 1 1 0)
3:  (1 0   1 0 1 1 0 0)
4:  (1 0   0 0 1 0 1 1)
5:  (1 0   1 1 1 0 0 0)
6:  (1 0   0 0 0 1 1 1)

7:  (0 1   0 1 1 0 1 0)
8:  (0 1   0 0 1 1 0 1)
9:  (0 1   0 0 1 1 1 0)
10: (0 1   1 0 1 1 0 0)
11: (0 1   0 0 1 0 1 1)
12: (0 1   1 1 1 0 0 0)
13: (0 1   0 0 0 1 1 1)
```


#### how is this obtained ?

you will find one line for each possible position of a piece on the board  
this line will contain:

- the first 2 columns (we have 2 pieces) correspond to the piece number  
  we set exactly one 1 to indicate which piece we're talking about  
  so for example the first 7 rows correspond to the 7 positions where we can place piece#0
- the next 6 columns correspond to the slots that the piece in that position would occupy  
  (1 means the slot is occupied)  
  and since the 2 pieces are identical, the 7 last rows carry the same information, but for piece#1

**NOTE** that obstacles in the board **must not** be given a column (there would bo only 0's in that column, and exact_cover would not find a solution)

and so for example with our small problem, the first line means:

- this is about piece#0 (hence col0=1 and col1=0)
- and that piece may be placed on the board in the following position

```
x 0 x
1 1 0
x 1 0
```

which, once you remove the obstacles, and flatten, reads `0 1 1 0 1 0`: the second half of first line


#### how to read a solution ?

the output of `exact_cover` in this case could be 

```
5:  (1 0   1 1 1 0 0 0)
13: (0 1   0 0 0 1 1 1)
```

which we then interpret, the other way around, like so:
- there is at least one solution to the problem
- and in this solution we have piece#0 that spans these locations
  ```
  x 1 x
  1 1 0
  x 0 0
  ```
- and piece#1 that spans these locations
  ```
  x 0 x
  0 0 1
  x 1 1
  ```


## what to do

### model the problem

decide how to represent the board and pieces:
* using nd-arrays, so rectangular spaces
* use only **booleans** to model **obstacles** in the board and the actual **contour** of pieces  

you will find some helper code in `data.py` if you wish to use it  
in particular, note the presence of `SMALL_BOARD` and `SMALL_PIECE`
that correspond to the following solution, and that may turn up useful for debugging your code

```{image} media/small-problem.png
:width: 150px
:align: center
```

### rotations and symmetries

for each piece, compute its - possibly up to 8 - variants

### compute all possible translations

for each piece (supposed to hve been rotated and/or swapped already)
compute all the possible locations on the board

### prepare the exact_cover input

given a board and a set of pieces, compute the input to `get_exact_cover()`

### pretty-print a solution

`exact_cover` will then compute one solution (if there's one, of course)  
from this solution, your job is to compute a 'pretty' view of the solution, something like e.g.
  ```
  (( 3  3  6  7  7  5  5  5 11 11 11 11)
   ( 3  6  6  6  7  9  5  5 10 11 12 12)
   ( 3  1  6  7  7  9  9 10 10 10 12  8)
   ( 3  1  1  4  4  4  9  9 10 12 12  8)
   ( 1  1  4  4  2  2  2  2  2  8  8  8))
  ```
  or, in the case where there are 'obstacles' on the board, it could be something like this
  ```
  (( 2  7  7  6 11 11 11 11)
   ( 2  7  6  6  6 10 11  4)
   ( 2  7  7  6 10 10 10  4)
   ( 2  5  5  0  0 10  4  4)
   ( 2  5  5  0  0  1  4  3)
   ( 8 12  5  1  1  1  9  3)
   ( 8 12 12 12  1  9  9  3)
   ( 8  8  8 12  9  9  3  3))
  ```

### matplotlib

if time permits, you could also transform this rough numpy solution into a nicer matplotlib drawing - or any other visual library of your choice, like e.g.

```{image} media/board-8x8-pretty.png
:align: center
:width: 60%
```

````{admonition} hints
utilise plt.imshow
to produce this we have
- used some predefined colormaps in matplotlib - see `matplotlib.pyplot.colormaps()` - you could consider accepting an argument that specifies one if them
- made the (color corresponding to) obstables transparent
- using the so-called alpha channel (fourth if you count first the red, green and blue channels)
````

```python
# import matplotlib
# matplotlib.pyplot.colormaps()
```


### testing

you should find at least one solution for
- rectangle 6x10
- rectangle 5x12
- rectangle 4x15
- rectangle 3x20
- rectangle 8x8 with a 2x2 obstacle in the middle
- 2 rectangles 5x6
- ... and many more of course, like e.g. `BOARD_8_9` in `data.py`


## links

* <https://en.wikipedia.org/wiki/Exact_cover>
* <https://en.wikipedia.org/wiki/Knuth%27s_Algorithm_X>
