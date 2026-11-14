# This Was Our Year — Anytime AI remix

A fictional alternate-history 2021–22 Lakers championship, with Russell Westbrook as Finals MVP and a championship ring. This did not happen in real NBA history. AI-generated music and pictures; fan-made, with no artist or NBA endorsement.

Reference: [Brian McKnight — Anytime](https://www.youtube.com/watch?v=AB3V0L5xrsM). Full uploaded reference: 0–276.048 seconds. One Mureka `mureka-9.5` remix via `POST /v1/song/remix`, `n=1`; observed music cost $0.50. Preservation of the source voice, melody and arrangement is a requested quality, not an exact API lock. No seed, temperature or numeric similarity setting is exposed.

## Exact music prompt

```text
One full-length faithful lyric-replacement remix of the supplied Brian McKnight Anytime recording. Preserve its lead vocal timbre, melody contours, original key, tempo, chords, piano/R&B instrumentation, drums, bass, backing vocals, phrasing, processing, mix, complete intro and overall arrangement as closely as possible. Sing ONLY the new lyrics: an explicitly fictional 2021-22 Lakers season, team chemistry, playoff wins, defeating Boston in Game 7, Russell Westbrook as champion and Finals MVP, ring and happy teammates. The ONE requested arrangement change: exactly ONE featured instrumental GRAND PIANO SOLO in the BRIDGE at the emotional Finals climax, no lead singing; breathtaking cascading double-time runs, thunderous left-hand octaves, jazzy extended chords, rapid arpeggios and a huge controlled crescendo. Return to the final vocal chorus for the championship/MVP celebration. No other solo sections. Warm emotional male R&B singing; no genre change. Full song, clean ending. One version.
```

## Supplied lyrics

```text
[Intro]
Purple and gold, a different story
This was our year

[Verse 1]
He came back home with a city to carry
Number zero, heart beating loud
Bron put an arm round his shoulder at practice
Said we're together, let's make them proud
Davis was soaring, they found one another
Melo was smiling, the corner was his
Monk lit the fourth and the whole bench was standing
Russ set the table, they learned how to win

[Chorus]
This was our year, we rose together
Purple and gold, all the way
Every last voice, every heart in the building
Knew we'd remember these days
Russell, you brought us home to the glory
Nobody carried this dream alone
This was our year, we rose together
Los Angeles, welcome him home

[Verse 2]
Reaves hit the floor for a loose ball in April
Dwight held the paint, they were locking it down
Round after round, they kept trusting each other
Russ found the pass when the pressure came round
Boston in June and the seventh game's burning
Down to the wire with the crowd on its feet
Bron draws the double and gives it to Russell
One final drive, now the city believes

[Chorus]
This was our year, we rose together
Purple and gold, all the way
Every last voice, every heart in the building
Knew we'd remember these days
Russell, you brought us home to the glory
Nobody carried this dream alone
This was our year, we rose together
Los Angeles, welcome him home

[Bridge - exactly ONE extended instrumental grand-piano solo; virtuosic cascading runs, thunderous octaves, emotional Finals climax; no lead vocals]

[Final Chorus]
This was our year, we rose together
Purple and gold, all the way
Clock hits the end, all his brothers surround him
Champions, tears on his face
Finals M V P, Russell is holding it
Bron and A D lift him high
Now there's a ring on his finger forever
Zero's our hero tonight

[Outro]
Melo is laughing, the whole team is singing
Gold in the air, all the love he has earned
One team, one dream, and a ring to remember
This was our year, this was our year
```

## Video and image inputs

[All 85 exact image prompts and hashes](visual-prompts.json), [three-second shot order](timeline.json), [video script](video-script.md), and [complete machine-readable recipe](recipe.json).

85 distinct generated images, 1080×1920, 30 fps, 4:13.070. Each image lasts 3 seconds except the final 1.070 seconds. The full generated intro is retained. Large 92px English lyric captions follow valid provider line timestamps; the same 46 cues are also published as a manual YouTube track. No pitch, tempo or gain change is applied by the renderer. Flat white/black strips are cropped before scaling to fill the frame; no padding, fades, blur backgrounds or color grading.

Fashion arrivals, gameplay/highlights, post-game interviews and team moments are interspersed through the season and championship payoff. The bridge contains the one requested piano solo; returned vocal timestamps leave a gap at 2:55.56–3:08.88. Lyric timestamps alone do not certify instrumentation. No extra solos are inserted or repeated by the video editor.

The intended 2021–22 roster and actual uniform references were checked. A few AI likeness/uniform artifacts remain in the existing frames, which were retained at the user's direction. Fashion and all imagined events are creative fiction. No claim that these are real historical photographs or exact outfits worn.

For the next narrative project: write the setup, setback/conflict, turning point and payoff before drafting the song and generating images. This existing song was approved without regeneration.
