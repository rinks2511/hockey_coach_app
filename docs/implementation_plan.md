# Substitution Planner Design

## The Mathematical Breakdown
You have **10 players**, and only **8 can play at a time**.
For a single **30-minute half**, this means:
- Total available playing minutes = 8 players × 30 minutes = 240 minutes.
- If divided equally among 10 players, each player plays exactly **24 minutes** per half and rests for **6 minutes**.

This divides a 30-minute half perfectly into **5 time blocks of 6 minutes each**:
- Block 1: 0 - 6 min (2 players rest)
- Block 2: 6 - 12 min (2 players rest)
- Block 3: 12 - 18 min (2 players rest)
- Block 4: 18 - 24 min (2 players rest)
- Block 5: 24 - 30 min (2 players rest)

By the end of the half, every single player has rested exactly once, and everyone gets exactly equal playing time! 

## Proposed UI Changes
Since you can already select players directly on the pitch tokens (using the small dropdowns), the right sidebar's "Squad Lineup" list is redundant. 

Instead, I propose replacing the sidebar with a **Substitution Matrix**:
1. **The Matrix:** A table with 10 rows (one for each player) and 5 columns (one for each 6-minute block).
2. **"Rest" Checkboxes:** You simply check the box for which block a player will rest.
3. **Auto-Validation:** The app will automatically highlight if a column doesn't have exactly 2 resting players, or if a player is scheduled to rest more/less than once.
4. **Integration with Save:** When you save the setup for "Half 1" or "Half 2", this substitution matrix will be saved alongside the tactical board. This way, the single artifact for "Half 1" acts as both your starting formation AND your substitution sheet for the entire half!

## Open Questions
- Do you like the idea of 6-minute substitution intervals, or would you prefer longer intervals (like 10 minutes) even if it means playing time isn't perfectly equal? 
- Should the matrix just track who is *resting*, or do you also want to track *which position* they substitute into when they come back on? (Tracking just the rest time is much simpler to use on the sideline).

Please review this plan and click "Proceed" or provide feedback!
