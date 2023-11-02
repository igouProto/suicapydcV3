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
There would be 5 parts of the jukebox:
- Queue system that extends Wavelink's queue
- Player that extends Wavelink's player to have more attributes (with the queue being one of them)
- Custom errors
- The jukebox (command interface)

### Facts I read from the Wavelink docs
- Played song would be popped from the queue (to be checked: pushed to the history queue?)
- Loop all = populate queue with history queue

### Thoughts
- Prev song command: dequeue from history queue, push that to queue, then skip
