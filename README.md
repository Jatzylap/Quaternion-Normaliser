 # Transformation Normaliser
Generates normalised transformation quaternions (decomposed / matrix form) for Minecraft display entities.

<img src="/src/thumbnail.png" alt="Image"/>

## Setup
- Run the script inside any command-line interface (Terminal for Mac / CMD for Windows)

## Basic information
Select between the decomposed `D` or matrix `M` (composed) modes to generate the corresponding quaternions to paste as transformation NBT in-game.

### Decomposed form
This relates to the default 14-float form of NBT assigned to Display entities `{transformation:{translation:[0f,0f,0f],scale:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f]}}` derived from a 4x4 affine rotation matrix. 
The program assumes that the sum of all squared input values (`x^2 + y^2 + z^2 + w^2`) is equal to 1 or sinθ(90).     

### Matrix form
This relates to the raw data stored in a 4x4 affine rotation matrix denoted as a 16-float equivalent to the decomposed form `{transformation:[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]}`. It is by far the most efficient way to compute Euler rotations as of Minecraft 1.20.
The program adopts an affine transform equation via matrix multiplication : `M' = M(t)M(s)M(θ)` (translation, scale, rotations) in vector component order (X -> Y -> Z -> W).

## Development information
Developed by: Jatzylap
> Python 3.12.3
