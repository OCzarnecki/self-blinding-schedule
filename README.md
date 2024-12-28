# Project

Generate a schedule of controls and interventions in runs, together with three sets of instructions.

A team of three can use these instructions to fill control and intervention into containers in a way that ultimately leaves them ignorant as to what is where. Two participants can also achieve this if they alternate to perform three roles.

The scripts outputs three files:
- `schedule_a.txt`: Instructions for the first participant. Fills half the cells with intervention or control.
- `schedule_b.txt`: Instructions for the second participant. Fills half the cells with intervention or control.
- `schedule_c.txt`: Instructions for the third participant. Permutes columns of cells.
- `truth.txt`: Final arrangement of control and intervention.

The program is currently configured to work with three sets of seven columns of four rows, because that's the pill orgainzers
we had when we wrote this.
