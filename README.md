# suicapydcV3
I'm forgetting Python so I'm rewriting Suica once again.

## Some notes to myself:
This rewrite (might be the last time) involves the following changes in design:
- Messages from Suica are now in Reples so no hard coding!
- Embeds should be implemented in the same way
- Music player embeds should be a separate module
- Extensions/Cogs now live in the Extensions directory
- Extensions should not be monolithic anymore
- Add custom prefix support?

## (Crude) plan to rewrite the Jukebox, facts from the docs and some thoughts
There would be 4 parts of the jukebox:
- Queue system that extends Wavelink's queue
- Player that extends Wavelink's player to have more attributes (with the queue being one of them)
- Custom errors in a class
- The jukebox (command interface)
- Player should be the only one accessing the Queue

## Functional Requirements of the Jukebox
### Must Have
- Connect / Disconnect
- Play
    - Searches for a song and:
        - Enqueue it when something is playing
        - Enqueue it
- Pause / Resume
- Display the queue
    - Queue has to be paginated
    - Tracks should be numbered
- Loop Control
    - Loop all
    - Loop one
- Volume Control

### Good to have (including something that's made possible with new Wavelink)

### Not important

## Misc.
### Facts I read from the Wavelink docs
- Played song would be popped from the queue (to be checked: pushed to the history queue?)
- Loop all = populate queue with history queue

### Thoughts
- Prev song command: dequeue from history queue, push what was dequeued to queue, then skip (make player stop so it grabs the next song)
