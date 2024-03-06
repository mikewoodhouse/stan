# Stan

## Sources

1. The Access database, containing details from end-of-season averages since 1947
2. The Excel spreadsheets, containing match-by-match data since 1994

## The Excel Season Averages Workbook(s)

In general, the following refers to the 2022 workbook, which is the most "highly-evolved" example...

### Worksheets (typical)

#### Matches

Top row summarises results, all automatic.

Row 5 for about 30 rows (2022: rows 5 to 32) are match details, after which there as some usful summary calculations. In the event of more macth rows being needed, I suggest inserting them before the last current match row so that the summary formulae will include the added matches without needing the referenced arrays to be adjusted (there are ways to mitigate this but as the author and expected sole user I didn't bother, assuming I'd be aware of any potential pitfalls here...)

Each row represents a match where at least one ball was bowled - if there was no play at all then the match isn't be considered for, e.g. appearances, even if everyone actually turned up!

##### Individual match rows

Start from the date (column B - the day of week is calculated and is mostly a hangover from the days of Saturday/Sunday/midweek games). Then fill in each column as far as X (opposition leg-byes).

Possible values for `Result` are W, L, D, T, ND (where the match did not reach a conclusion, usually because of rain).

The `notes` columns (J and N) are free txt, for anything considered noteworthy. Purely subjective. Not used for anything at present but may be presented in the "Stan" website if it ever gets finished.

`Queries` (column AE) has been used on occasion where I needed to go back to someone who was at the match to get more information, usually because something was missing or unclear in the book.

Columns AF to AH were added to record the numbers of runouts (and for Trinity players, the identities of the dismissed batsmen) in order to make summarising that information in the "Notes" section at the end of the averages easier to compile.

#### Batting

Rows 1-4 are a link from the `Matches` worksheet.

From row 5 there is a row for each player who has appeared in a match. I usually start with the list from the previous season and add new players as they turn up during the season. I include anyone who has made an appearance, regardless of whether they batted, because this worksheet is also the source for appearance and fielding statistics.

New players are added by inserting rows in an appropriate location. Note that the stats summary table to the right of the player-match data will need the formulae to be copied, typically from the row above or below, it doesn't matter exactly where, the references should all update to act on the newly-inserted row.

I tend to keep the list in alphabetical order to help me locate individuals, but it's not a requirement.

The exact location of the stats table may vary from season to season - it's somewhat dependent on the number of matches played, in that I may have removed some columns in later years when we weren't playing 60 matches any more.

##### Player performance input

Each player's performance for a match is recorded here in a string, delimited by `/`s as follows:

| field            | notes                                                                  |
| ---------------- | ---------------------------------------------------------------------- |
| batting position | as listed in the scorebook, taking account of amendments where present |
| runs scored      | use 0 if player did not bat                                            |
| how out          | `how  out` + `captain`  + `kept wkt` (see table below)                 |
| fielding         | `catches.stumpings`                                                    |
| boundaries       | `fours.sixes`                                                          |

**How out, etc***:  IMPORTANT - this field is also used to mark captain (with `*`) and wicket-keeper (`+`). More than one player may have kept - they all get the `+` notation

**Fielding**: For outfielders, the number of catches they took is sufficient. For 'keepers, also add stumpings as a "decimal", e.g. `2.1` would indicate 2 catches & one stumping. Catches taken in the outfield by a player who also kept wicket are considered as wicket-keeper catches because the scorebooks seldom contain sufficient detail to distinguish between them, if indeed it's ever happened...

**Boundaries**: a digit on its own means fours and no sixes. Enter a `0` if no boundaries (the macros aren't smart enough to cope with an empty value)

Examples:

`3/64/b*+/0.1/13.0` - batted at3, scored 64 and was bowled. Was captain and kept wicket, taking no catches but one stumping and hit 13 fours but no sixes.

`9/0/dnb/0/0`: Played, listed in the scorebook at #9 but did not bat and took no catches.

| How Out | description                                                    |
| ------- | -------------------------------------------------------------- |
| no      | Not out                                                        |
| dnb     | Did not bat                                                    |
| b       | Bowled                                                         |
| c       | Caught                                                         |
| lb      | LBW                                                            |
| st      | Stumped                                                        |
| ro      | Run Out                                                        |
| hw      | Hit wicket                                                     |
| ret     | Retired out - I believe I'd record "retired hurt" as "not out" |

##### Match summary rows

Below the player-match performance section there are some calculations for helping with reconciliation:

`Captain` records the number (hopefully 1) of entries with a `*` - the scorebook doesn't always record who was captain and it's not always obvious.

`Wkt` does the same for `+`. Again, it's not always clear who kept wicket - competent scorers are a scarce breed these days. Note that there may have been more than one 'keeper in a match.

`Total bat runs`: total runs indicated by the player entries for the match

`Opp extras`: linked from the `Matched` sheet

`Total Runs`: Sum of the above, should match the `TOCC Runs` column in the `Matches` sheet, but often will not, sometimes dramatically, see comment about competent scorers above.

Below that, some further summary information that may or may not be useful. The big table helped me to pick out, e.g. players who scored 50s (in the 2022 workbook at least, others may vary, I can't remember!)

##### The player summary section

Summarises everything to the left. Parts are linked to, e.g the `BatAves` sheet.

In the most recent workbook (2022 at time of writing) at least, I added a section at the far right that can be copied to `To_Word_Doc` for sorting into presentation-worthy (or close to it) tables.

#### Bowling

Works in a very similar fashion to `Batting` above: matches in the top rows, players at the left, although this time only players who actually bowl (or who at the start of the season bowled previously or might reasonably be expected to bowl) tend to be included.

##### Bowling performance input

Each player's performance with the ball for a match is recorded here in a string, delimited by `/`s as follows:

| field         | notes                                                                          |
| ------------- | ------------------------------------------------------------------------------ |
| over/balls    | as listed in the scorebook, add '.' and the number of balls bowled if not zero |
| maidens       | use 0 for none, I don't think the macro likes an empty string here             |
| runs conceded | as per scorebook                                                               |
| wickets taken | as per scorebook                                                               |

In this instance it's possible to key the entire input value using the numeric keypad alone, which (if one has a keyboard with the facility) makes the process relatively painless.

##### Summary/Reconciliation

Below the player rows is another "reconciliation" section, summarising runs conceded according to the bowling performances above and combining them with the corresponding extras values from the `Matches` sheet. Total overs/balls ought to match the `Matches` sheet as well - there's conditional formatting on the linked cells that shows red to indicate a difference.
As with batting, these may not always agree and careful scrutiny of the scorebook *may* (but often will not) reveal an error, either in the source or in the input (nobody's perfect). Often, however, things just don't add up and it's not possible to determine in which section the difference has arisen. Turns out good scorers are a scarce and valuable resource....

The table below is one I used from time to time to help spot useful items: for example, in the 2022 workbook I wanted to check for any five-fors, which I handled by setting cell B59 to `=WicketsTaken` (maps to a constant value of 4) and pulling the relevant figure from each performance. `B58` shows the highest value thus extracted (4 in this case) which told me that nobody in 2022 actually managed to take 5 wickets in an innings (bring back time games and unrestricted over counts!)

##### The player summary section

Summarises everything to the left. Parts are linked to, e.g the `BowlAves` sheet.

#### Partnerships

I make a note of any partnership that might be worth reporting, all of (I think) 50 and above (or is it 75?) plus anything else noteworthy, especially at the tail end. Inputs go in acolumns A-J:

| Col   | Heading     | Description                                                                                                     |
| ----- | ----------- | --------------------------------------------------------------------------------------------------------------- |
| A     | Match       | Index to `Matches` sheet, fills in columns K & L                                                                |
| B     | Wkt         | Which wicket the partnership represented                                                                        |
| C     | Total       | Partnership runs                                                                                                |
| D     | Unbtn       | '*' if both batsmen were not out, otherwise leave blank                                                         |
| E     | Bat1        | Score for the first batter - I tend to make this the one appearing earlier in the order (doesn't really matter) |
| F     | Sc1         | Runs for batter 1 from scorebook                                                                                |
| G     | NO          | '*' if batter 1 was not out                                                                                     |
| H,I,J | Bat2/Sc2/NO | Batter 2, as above                                                                                              |


#### BatAves

#### BowlAves

#### Capts

#### (other)

##### To_Word_Doc

##### Scratchpad

If present, it's just somewhere I might use to dump, sort and format data before copy-pasting it into Word. Clear it, fill it up, cover it with graffiti, whatever.

#### Macros

The important module is `modFuncs` and the important functions are described (briefly) below. These were written about 30 years ago and I'd say they're very much not what I'd produce now. I haven't bothered to go back to them, however, because by and large they've done the job without ever needing modification, apart from when I removed the Fantasy Cricket points calculations some years ago.

##### `BowlSplit(Inval, intWhich As Integer)` & `BatSplit(Inval, intWhich As Integer)`

`Inval` is a range describing the player performance string(s) as described above. `intWhich` is an integer that defines the value to be returned. The workbook has named formulae (behaving as constants) that save having to remember which stat is returned for which number. Use `Formulas|Name Manager` to see the full list of constants thus defined, or examine individual cell formulae for specific values. The constants are also defined at the top of `modFuncs`.