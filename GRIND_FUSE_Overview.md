# GRIND//FUSE — Project Overview 😈

> A rank-forging collectible **auto‑battler** where players grind, fuse, and climb absurd power tiers. Designed to be **AI‑operable** end‑to‑end, with a light human touch for taste and oversight.

---

## 1) Elevator Pitch
Open packs → fight quick auto battles → hoard duplicates → **fuse 10→1** up brutal ranks (E→F→D→C→B→A→S→SS→SSS). The fun: completing sets, beating stronger tiers with synergies, and watching numbers explode as you ascend.

**Target session length:** 3–10 minutes  
**Platforms:** WebGL (itch/Steam playtest), desktop later  
**Audience:** Collectors, tinkerers, idle/auto‑battler fans, goblins who love big numbers

---

## 2) Core Player Loop
1. **Battle** (30–90s, auto): pick a 3‑unit squad, press Start, watch it bonk.  
2. **Loot:** win = cards + shards; loss = pity + shards.  
3. **Fuse:** 10 copies (same card & rank) → 1 of next rank.  
4. **Unlock:** higher ranks gate dungeons, themed packs, cosmetics.  
5. **Repeat** with missions/events/leaderboards nudging goals.

---

## 3) Rank Model (the 10× gospel)
Let ranks index upward with E=0, F=1, … SSS=8.

- **Power:** `power(rank r) = base_power * 10^r`  
- **Fusion:** `10 of rank r → 1 of rank r+1`  
- **Cumulative E‑equivalents:** F=10E, D=100E, C=1,000E, B=10,000E, A=100,000E, …

This creates huge perceived gaps—perfect for satisfying “impossible → sudden breakthrough” moments.

---

## 4) Systems the AI Can Operate Today

### 4.1 Card Generator
- **Inputs:** theme (e.g., “Dungeon Depths”), role (tank/dps/support), rarity target.  
- **Outputs:** card JSON (below), art tags, flavor line.  
- **Guards:** ability budgets, trait diversity, overlap limits.

```json
{
  "id":"slime_knight_001_E",
  "display_name":"Gelatinous Page",
  "set":"Dungeon Depths",
  "rank":"E",
  "rarity":"Common",
  "role":"Tank",
  "stats":{"atk":1,"hp":6,"spd":0.8},
  "ability":{"id":"absorb_split","text":"Absorb damage equal to DEF each round. On death, spawn 2 Mini-Slimes."},
  "traits":["ooze","knight"],
  "art_tags":["green slime","battered pauldron","torchlit corridor"],
  "flavor":"Once a squire. Now mostly pudding."
}
```

*Fusion versions:* same family id with rank suffix (`_F`, `_D`…), scaled stats, evolved art tags & ability line.

### 4.2 Packs & Pity
- **Pack types:** Core (broad, cheap), Themed (boosted set odds), Ranked Cache (one‑below guarantee after beating a dungeon).  
- **Example odds:** Common 65%, Uncommon 25%, Rare 8%, Mythic 2%.  
- **Pity:** Rare guaranteed at 10th pack without Rare; Mythic at 30th without Mythic.  
- **Duplicate soft‑protection:** avoid 11th copy when 10 complete a fuse.

### 4.3 Fusion & Upgrades
- **Card fuse:** 10 copies (same card & rank) → next rank.  
- **Wildcards:** convert dupes via events into family‑bound wildcards (e.g., “any slime”).  
- **Ascension (A+):** consume 3 same‑rank copies to add +stars (+~5% stats per star, capped).

### 4.4 Combat (Auto, Readable, Tunable)
- **Format:** 3v3 lane brawler; basic pathing; cooldown abilities; simple focus rules.  
- **Target clear rate:** 55% at equal total power; AI tunes enemy HP/ATK ±5% to hold target.  
- **Synergies:** tags unlock passives (e.g., `[ooze x2]` regen, `[knight x2]` +DEF).  
- **Boss quirks:** single rule pushes roster variety (e.g., “punishes duplicates”).

### 4.5 Events & LiveOps
- **Weekly Theme** (e.g., “Crystal Catacombs”): reskinned packs, 15–25 rotated cards, 3 short quests.  
- **Mini‑Arc (2 weeks):** temporary modifier + new family with a chase Mythic.  
- All copy/art prompts can be AI‑generated then lightly reviewed.

### 4.6 Auto‑Balancing Loop
- **Headless sim:** 10k battles per tier across meta & randomized squads.  
- **Tuning:** adjust enemy multipliers to maintain 55% parity winrate.  
- **Pacing:** track **E‑equivalents/hour**; nudge rewards ≤5% weekly to hit “Days‑to‑A” targets for Casual (30m/day) vs Grinder (2h/day).  
- **Stability rail:** patch deltas capped (±12% difficulty swing/week).

---

## 5) Data Schemas

**Rank config**
```json
{"ranks":["E","F","D","C","B","A","S","SS","SSS"], "fusion_cost":10, "power_base":1}
```

**Card (normalized)**
```json
{
  "id":"<family>_<num>_<rank>",
  "display_name":"",
  "set":"",
  "rank":"E",
  "rarity":"Common|Uncommon|Rare|Mythic",
  "role":"Tank|DPS|Support",
  "stats":{"atk":0,"hp":0,"spd":1.0},
  "ability":{"id":"","text":""},
  "traits":[],
  "art_tags":[],
  "flavor":""
}
```

**Pack**
```json
{
  "pack_id":"core_v1",
  "cards_per_pack":5,
  "rarity_odds":{"Common":0.65,"Uncommon":0.25,"Rare":0.08,"Mythic":0.02},
  "pity":{"rare_at":10,"mythic_at":30},
  "rank_bias":{"at_or_below_player_top":0.8,"one_below_guarantee":1}
}
```

**Battle log (telemetry)**
```json
{"t":"battle_end","dungeon":"D-2","win":0,"player_pp":132,"enemy_pp":140,"turns":9,"top_card":"slime_knight_001_F","deaths_by":["bleed","ignite"]}
```

**Economy ledger**
```json
{"t":"reward","kind":"pack_open","cards":[/* ids */],"ee_gain":124,"source":"event_weekly"}
```
> **EE (E‑equivalents):** convenient unit for pacing math.

---

## 6) Content & Repo Structure
```
/Content
  /Cards        # JSON by set/family; deterministic seeds
  /Packs        # odds, pity, rotations
  /Dungeons     # tiers, boss quirks, enemy multipliers
  /Localization # en/* with autogenerated stubs
  /Art          # prompt templates + generated renders
/Sim
  headless_runner/  # battle sim; emits CSV telemetry
  balance_agent/    # ingests CSV, rewrites Dungeons.json
/Client
  # Godot or Unity project (see Tech Stack)
/CI
  build.yml  # GitHub Actions → WebGL; deploy to itch via butler
```

---

## 7) MVP Scope & Timeline (2 Weeks)

**Week 1**
- 3v3 combat prototype; 1 dungeon tier (E–D).  
- 20 cards across 3 families; fusion UI; packs + pity.  
- Headless sim + balancing loop; WebGL build.

**Week 2**
- Add A‑gate dungeon; first Event (“Ooze Week”); 3 quests; leaderboard (time‑to‑clear).  
- Telemetry dashboards (winrate by tier, EE/hour, time‑to‑B/A).  
- Soft duplicate protection; basic accessibility pass.

---

## 8) Monetization & Fairness Guardrails
- **No direct A/S drops in early game**; one‑below guarantees only.  
- **Wildcards:** weekly cap; Mythic non‑wildcardable.  
- **Visible pity counters**; no stealth mid‑week odds changes.  
- **Auto‑stabilizers:** if median time‑to‑A < target by >20%, reduce EE/hour by ~3% via quests (not raw pack odds).  
- **F2P friendly:** dailies grant packs; paid cosmetics (card frames, board skins) are clean revenue without power creep.

---

## 9) Telemetry KPIs
- **Winrate@Parity:** hold ~55% per tier.  
- **EE/hour:** casual vs grinder profiles.  
- **Days‑to‑Milestone:** E→F→D→C→B→A.  
- **Collection Health:** #uniques, duplicate overflow, wildcard burn.  
- **Event Impact:** lift in sessions, pack opens, retention D1/D7.  
- **Economy Stability:** variance of time‑to‑A across cohorts.

---

## 10) Accessibility & Compliance
- Colorblind‑safe palettes; readable fonts; seizure‑safe VFX.  
- Remappable controls; screen‑reader labels for UI.  
- Clear odds disclosure + pity terms; audit asset provenance (AI‑generated originals only).

---

## 11) Tech Stack
- **Engine:** Godot (GDScript) or Unity (C#).  
- **Data‑first:** JSON content; deterministic ids & seeds.  
- **CI/CD:** GitHub Actions → WebGL; itch deploy.  
- **Art:** prompt‑to‑image with fixed style guide & upscaler.  
- **Sim:** Headless runner (CSV) + balancing agent (Python).

---

## 12) Risks & Mitigations
- **Polish gap:** Auto content ≠ juicy feel → budget time for screenshake, VFX, input buffering.  
- **Content drift:** Agents wander → strict schemas, linting, unit tests on JSON.  
- **Economy inflation:** Watch EE/hour + pity abuse → weekly clamps, visible counters.  
- **Legal/IP:** Originals only; log model/source + prompts/seed per asset.

---

## 13) Sample Cards (First Pass)
- **E:** Gelatinous Page (tank), Torch Moth (support regen), Pebble Imp (taunt)  
- **F:** Ooze Yeoman (thorns), Ember Newt (ignite), Gravel Golem (shield)  
- **D:** Royal Slime (split+taunt), Fire Salamancer (ignite chain), Stone Knight (barrier)  

---

## 14) Glossary
- **EE (E‑equivalents):** total grind currency normalized to E‑rank units.  
- **One‑below guarantee:** packs guarantee drops at your top rank − 1.  
- **Ascension Stars:** post‑A incremental upgrades consuming duplicates.

---

## 15) Next Steps (Pick One)
1) Stand up repo skeleton + sample JSON + mock battle runner.  
2) Build pack‑opening + fusion demo (WebGL).  
3) Integrate headless sim + balancing loop; ship public playtest.

> Ping me which path you want, and I’ll spin up the scaffolding. Let’s make those numbers thicc. 💪😏
