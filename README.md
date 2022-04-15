# Window Input Pong

An input system for [r/badUIbattles](https://www.reddit.com/r/badUIbattles/)

[Reddit post here](https://www.reddit.com/r/badUIbattles/comments/u3zflq/window_input_pong_each_element_is_a_separate/)

Inspiration: [u/Ill-Chemistry2423's comment](https://www.reddit.com/r/badUIbattles/comments/tyr7qx/comment/i3v07k8) on [u/letternumsymboldash's Windows Pong post](https://www.reddit.com/r/badUIbattles/comments/tyr7qx/windows_pong/)

## Usage
Pygame is required: `pip install pygame`

`python main.py`

Use arrows to move paddle. If it hits an inner region, the selection will move one space in the indicate direction, and five for outer regions. Miss to type the selected letter.

Special characters:
 - ⌫: Delete the previous character.
 - ⇬: The next letter typed will be uppercase.
 - ⏎: Finalize your input.
 - ⎚: Clears the input.

If you see the symbols as boxes, install [Symbola Font](https://zhm.github.io/symbola/)

