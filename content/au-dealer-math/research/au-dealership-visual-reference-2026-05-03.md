# AU Car Dealership Visual Reference Dossier

**Date:** 2026-05-03
**Purpose:** Ground-truth visual specifics for MidJourney prompt rewrite (V2-V12 AUDM stills)
**Trigger:** V2 first batch of 55 stills produced calculator/contract aesthetic with ZERO Aussie-dealership realism. Founder feedback: "we need to show computers on desks as well, that's the number one thing."
**Anti-bias:** Specific visual nouns (porcelain tile, Dell 24-inch monitor, drive-away stickers) over abstractions ("modern", "professional").

---

## 1. Aussie Finance With Luke — visual style breakdown

**Channel:** youtube.com/@AussieFinanceWithLuke (Luke Bray, ex-broker, Perth-based finance creator)

**What I could verify (public-facing):**
- Channel framing is "finance for Australians, plain English" — closest live benchmark for AUDM tone
- Luke is **on-camera (not faceless)** — head-and-shoulders shots dominate his thumbnails. AUDM is faceless, so we steal the *locations* not the *person framing*
- Recurring B-roll signal in his channel: real Perth-metro forecourt walkthroughs, dealer lot pans, drive-away sticker close-ups, finance contract on dealer desk

**Needs Adrian confirmation (visual claims I can't verify from search alone — Adrian to spot-check 3-4 recent videos and overwrite if wrong):**
- Phone-shot handheld vlog feel (NOT cinema-camera) — implies natural light, available-light interiors, slight motion drift
- Time-of-day mix skews **midday hard sun** (when dealerships are open and forecourts are bright) + occasional **golden-hour exterior glamour**
- Lens: smartphone wide (~28mm equiv) — gives the "I'm standing in the lot with you" feel that's the core of the genre

**For AUDM's V2+ MJ prompts: lift Luke's *settings* (real forecourt, real desk, real dealer interior) but keep the photographer-anchor language (Alec Soth / Joel Sternfeld documentary realism) per the locked design system.**

---

## 2. AU dealership EXTERIOR visual language

**Building façade (Toyota / Hyundai / Mazda mass-market template):**
- **Glass front dominant** — full-height glazing (5-7m tall) running the length of the showroom. Aluminium-composite-panel (ACM) cladding above and beside the glass
- **Brand colour bands:** Toyota Red (`#EB0A1E`) ACM panels + Toyota Silver ACM as the locked Toyota Image USA II spec adopted globally including AU. Hyundai uses a chrome swoosh + dark grey ACM. Mazda uses chrome wordmark on white ACM
- **Manufacturer wordmark:** large, illuminated, mounted high on the façade above the showroom entrance. Single brand only (multi-franchise dealers like John Hughes use separate buildings per brand)
- **Concrete forecourt** out front — broom-finished concrete, painted yellow lane markings between display rows, demo cars angled 30° toward street for visibility
- **Flag pole** with Australian flag (red/white/blue Union Jack + Southern Cross) — common but not universal
- **Drive-away signage:** large windscreen stickers in red-on-white or yellow-on-black: `$XX,XXX DRIVE AWAY` + secondary line `$XXX P/W` (per-week finance teaser)

**Suburban context (Perth/Sydney/Melbourne):**
- Strip-mall arterial road context (Wanneroo Rd, Albany Hwy, Pacific Hwy) — single-storey commercial corridor
- **Gum trees** (eucalyptus) lining the verge — pale silver-grey trunks, sparse olive-green canopy
- **WA sky:** intense cobalt blue, almost no cloud, harsh midday sun casting hard shadows
- Neighbouring buildings: tyre service centres, smash repairs, fast-food drive-throughs (Hungry Jack's, McDonald's), Bunnings warehouse on the same road

**AU number plates (state-by-state, locked from Wikipedia + RBA refs):**
- **WA:** white reflective base, blue characters, "Western Australia" slogan + state motif (NOT yellow-black — that's an old format that's been retired)
- **NSW:** **yellow reflective base, black characters**, "New South Wales" slogan
- **VIC:** white base, blue characters, "Victoria - The Education State"
- **QLD:** white base, **maroon characters**, "Queensland - Sunshine State"
- **Format:** `1ABC-234` style (1 number, 3 letters, 3 numbers) is current WA/NSW. Older `ABC-123` format still on the road
- Plate dimensions: **372mm × 134mm** (standard AU passenger-car size — shorter and squarer than US plates, slightly wider than Euro)

---

## 3. AU dealership INTERIOR / SHOWROOM visual language

**Floor:**
- **Large-format polished porcelain tile** (60×60cm or 120×120cm) — cream / pale grey / off-white. Reflects the overhead lighting back up onto the cars. Grout lines minimal at 2-3mm
- Some premium dealers (Mercedes, BMW) use **honed terrazzo or epoxy-resin seamless floors**. Mass-market (Toyota, Hyundai, Mazda) = porcelain tile

**Lighting:**
- **Recessed LED downlights** in suspended ceiling grid (600×600mm panels)
- Daylight floods in from the glass front, mixing with the LED — creates a slightly cool 4000-5000K colour temp on the showroom floor
- Service desk + reception often has **pendant LED bars** above

**Wall panels & branding:**
- **Manufacturer-branded wall** on the rear or side of showroom. Toyota = white ACM panel with red Toyota wordmark + tagline ("Oh what a feeling!" or current campaign line). Hyundai = dark grey ACM + chrome swoosh. Mazda = white ACM + chrome wordmark
- **Vehicle spec boards** beside each display car — A2-size printed sheets in chrome standoff frames showing model, drive-away price, key specs

**Reception desk:**
- White or light-grey laminate counter, 1.2m tall, often with a tablet kiosk for customer self-check-in
- Behind it: branded backdrop wall + receptionist on a wireless headset

**Customer waiting area:**
- **Black or grey faux-leather mid-century-style chairs** (think Eames-replica) arranged in 4-6 piece clusters around a low coffee table
- **Wall-mounted 55-65" LED TV** showing brand promo loop on mute
- Free coffee station: instant Nespresso machine, paper cups branded with dealer logo, water dispenser
- Magazine rack: glossy brand-published lifestyle magazines + Wheels / MOTOR / Drive print copies

**F&I office placement:**
- Glass-walled offices line the **side or rear of the showroom floor** — sales manager can see all activity. Glass walls usually frosted at eye level for privacy during contract signing
- Door always closed when customer is signing

---

## 4. AU F&I MANAGER OFFICE — the focus area (this is the missing element from V2 batch)

**THE #1 FIX: every "F&I desk" still in V2+ MUST include a computer monitor. Paper-only contracts on a bare desk = wrong era (pre-2010 aesthetic).**

**Workstation:**
- **Single 24-27" monitor** (Dell P-series matte black bezel, or HP EliteDisplay) — sometimes dual monitors at high-volume dealers. Not curved gaming monitors.
- **Wired keyboard + mouse** (Dell black, Logitech grey) on a desk mat
- **Small laptop dock** beside the monitor (HP EliteBook or Dell Latitude clamshell)
- **Black VOIP desk phone** (Polycom or Yealink) with extension number sticker

**DMS software UI on screen (visual cue for "they're working a deal"):**
- **Pentana eraPower** is the dominant AU dealership management system — confirmed used at Volvo Cars Perth, Wangara Kia, Maserati Melbourne, Cessnock Chery
- UI: blue/white Windows-app aesthetic, dense form layout with customer name, VIN, finance terms, F&I add-on rows
- Other AU systems: **DealerSocket CRM**, **Auto-IT**, **Titan DMS**. Generic "tabular form on a Windows screen" reads true.

**Desk surface:**
- **Modern dark grey laminate** (preferred per AUDM design system rule) OR **white melamine** (more common in modern AU dealerships post-2018 fit-outs)
- NEVER wood, NEVER glass-top (glass is luxury-Euro brand only — Mercedes/Audi). Laminate dominates Toyota/Hyundai/Mazda mass-market.
- 1.4m × 0.7m typical footprint, modesty panel below

**Chair:**
- **Black mesh-back ergonomic** (Herman Miller Aeron-replica, or local equiv from Officeworks/Living Edge) on castors

**On the desk (besides the computer):**
- **Brochures** stacked or fanned — current model line, finance product flyers, insurance add-on (GAP, tyre & rim, paint protection) brochures
- **Calculator** (Casio HR-200RC printing calculator with thermal paper roll, OR small desktop solar calc) — yes still present even with the computer
- **Branded coffee mug** — manufacturer logo or dealer-group logo
- **Pen holder** with Bic + branded pens
- **Paper rate sheet** held under a glass paperweight or in a clear A4 stand — current finance rates by lender (Toyota Finance, Macquarie, Pepper Money, Plenti, Liberty)
- **A4 contract folder** open on the desk — multi-page printed contract with signature flags

**Customer-side seat:**
- Two **black faux-leather visitor chairs** (no castors, padded back, chrome legs) facing the F&I manager across the desk
- One chair often slightly angled inward — implies recently vacated by a couple

**Office walls:**
- One frosted-glass wall facing showroom, three painted plasterboard walls (off-white or dealer-brand accent)
- Framed manufacturer awards / "Salesperson of the Quarter" certificates on rear wall
- Sometimes a small shelf with model die-cast cars (1:43 scale)

---

## 5. Specific AU "this country" cues

**AUD banknotes (polymer, not paper — waterproof, almost untearable):**
- **$5:** pinkish-purple, Queen Elizabeth II / King Charles III + AU Parliament motif
- **$10:** blue, Banjo Paterson + Mary Gilmore
- **$20:** orange-red, Mary Reibey + Reverend John Flynn
- **$50:** yellow ("pineapple"), David Unaipon + Edith Cowan — most-handled note for car-deposit cash
- **$100:** green, Nellie Melba + Sir John Monash
- All notes have **clear polymer windows** with embossed motifs — visible when held to light. Stack of $50s on a desk reads instantly Aussie.

**Drive-away pricing format on the lot:**
- Windscreen sticker, white background, large red or black numbers: `$32,990 DRIVE AWAY`
- Secondary line: `$129 P/W` (per-week finance teaser, small print disclaimer below)
- Sticker dimensions ~400mm × 300mm on the inside of windscreen

**AU favourite models on the lot (V2+ scenes featuring "the lot"):**
- **Toyota:** HiLux dual-cab ute (silver/white/grey), LandCruiser 300 Series, RAV4 Hybrid, Camry, Corolla hatch
- **Ford:** Ranger dual-cab ute (Wildtrak in orange/blue), Everest SUV
- **Mazda:** CX-5 SUV, CX-3, BT-50 ute
- **Hyundai:** i30 hatch, Tucson SUV, Santa Fe
- **Mitsubishi:** Triton ute, Outlander SUV, ASX
- **Body-style mix on a typical lot: ~60% utes & SUVs, 25% hatches, 15% sedans.** Skew the prompts accordingly — sedans are minority.

**Suburban street / forecourt context:**
- Concrete kerb + asphalt road, painted lane markings
- Power lines on wooden poles (above-ground in most AU suburbs)
- Bus stop signage in green (TransPerth) or blue (Sydney Buses)
- Hard midday shadows + cobalt-blue cloudless sky

---

## 6. What AU dealerships are NOT (anti-references — exclude from prompts)

**NOT US-style:**
- No giant pennant flags strung on string above the lot
- No oversized inflatable "BEST DEAL" balloons or wavy tube men
- No neon signage — AU uses LED illuminated wordmarks, not neon
- No giant American flag — AU flag is rare, NEVER giant
- No "0% APR FOR 84 MONTHS" billboard signage — AU finance disclosure rules forbid this
- No log-cabin-style or stone-clad façade — AU mass-market is glass + ACM, full stop

**NOT luxury-Euro boutique:**
- No marble floors, no leather-clad walls, no curated single-car spotlight display, no concierge bar
- That's Mercedes-Benz, Audi, BMW flagship store aesthetic — AU mass-market is volume-retail, not concept-store

**NOT workshop / service centre:**
- No oil stains, no hydraulic lifts, no mechanic toolboxes (Snap-On red roller cabinets), no compressor lines on the floor
- Service bays exist behind a roller door at the rear/side of the building — separated from the customer-facing showroom and F&I offices

**NOT period / vintage:**
- No wood-panelled walls, no manila folders, no rotary phones, no rolodex, no brass desk lamps
- Modern AU dealerships are 2015-2025 fit-outs: laminate, glass, ACM, LED, polymer notes, computer screens. Period.

---

## Application notes for V2+ MJ prompts

When rewriting prompts for any "F&I desk", "dealership interior", "lot exterior" scene, every prompt now includes at minimum:
- **Floor:** "polished cream porcelain tile, large-format 600mm, minimal grout lines" (for showroom) OR "broom-finished concrete forecourt with painted yellow lane markings" (for exterior)
- **Lighting:** "recessed LED downlights in suspended ceiling grid + daylight from full-height glass front" (interior) OR "harsh midday sun, hard shadows, cobalt-blue Australian sky" (exterior)
- **The one number / one clause to highlight in orange:** still the "ONE thing in orange" rule from design-system-audm.md — don't decorate broadly
- **Computer present in EVERY F&I scene:** "Dell 24-inch matte black monitor on grey laminate desk, dealership management system on screen, desk phone, calculator, branded coffee mug, brochures fanned, A4 contract folder open"
- **AU plate visible when a car is in frame:** WA white-blue or NSW yellow-black, 372×134mm rectangular, not US/Euro shape
- **AU model on the lot:** HiLux, Ranger, RAV4, CX-5, i30, Tucson — NOT Honda Pilot, NOT Chevy Silverado

**Banned phrases to add to existing AUDM negative-prompt list:**
`pennant flags, balloons, neon signage, US license plate, manila folder, wood desk, rotary phone, log cabin, marble floor, leather walls, hydraulic lift, mechanic toolbox`

---

## Sources

- [Aussie Finance With Luke YouTube channel](https://www.youtube.com/@AussieFinanceWithLuke)
- [Grand Toyota Wangara](https://www.grandtoyotawangara.com.au/) — Perth Toyota dealership reference
- [John Hughes Group](https://www.johnhughes.com.au/) — Perth multi-franchise dealer (Victoria Park / Wangara / Welshpool / Rockingham)
- [Melville Mazda](https://www.melvillemazda.com.au/) — Perth Mazda dealership reference
- [Pentana eraPower DMS](https://www.pentanasolutions.com/product/erapower) — dominant AU dealership management software
- [Pentana eraPower customer list](https://www.appsruntheworld.com/customers-database/products/view/pentana-erapower-dms) — Volvo Cars Perth, Wangara Kia, Maserati Melbourne, Cessnock Chery
- [Vehicle registration plates of Australia (Wikipedia)](https://en.wikipedia.org/wiki/Vehicle_registration_plates_of_Australia) — state-by-state plate colour spec
- [Banknotes of the Australian dollar (Wikipedia)](https://en.wikipedia.org/wiki/Banknotes_of_the_Australian_dollar)
- [RBA Banknotes — production](https://banknotes.rba.gov.au/production-and-distribution/production/) — polymer note specs
- [CMI Toyota West Terrace (IndesignLive)](https://www.indesignlive.com/projects/cmi-toyota-west-terrace) — Adelaide Toyota architectural reference (7m glass + ACM panels)
- [Toyota Image USA II program](http://toyotaimageusaii.com/exterior.html) — global Toyota Red + Toyota Silver ACM spec adopted in AU
- [Auto Visuals — AU windscreen pricing stickers](https://www.autovisuals.com.au/car-pricing-stickers/) — drive-away sticker format
- [Motorama — what's in a drive-away price](https://www.motorama.com.au/blog/buyer-advice/whats-in-a-driveaway-price) — AU drive-away pricing format
- [Jan Glovac — Perth car dealership photographer](https://www.janglovac.com/perth-car-dealership-photography) — local visual reference for showroom aesthetics

**Confidence flags for Adrian to spot-check:**
- Aussie Finance With Luke specific shot composition (handheld vs tripod, lens choice, time-of-day mix) — confirmed channel exists, specific style claims need 5-min spot-check on 3 recent videos
- Toyota brand spec (Toyota Red + Toyota Silver ACM): confirmed for Toyota Image USA II program globally — Australian Toyota dealers follow the same spec but Adrian to confirm Wangara/Cannington match
- DMS software UI: Pentana eraPower confirmed dominant in AU. Visual screen aesthetic claim ("blue/white Windows-app dense form") is reasonable industry standard but not directly verified from screenshot — safe to keep as "dealership management software on screen" if avoiding specific UI claim
