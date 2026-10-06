# Flow — Create and render (F2, F3)

- Trigger: the user opens a task screen.
- Covers: AC-10, AC-11, AC-12, AC-20, AC-21, AC-22, AC-23.

## Steps
1. User fills the inputs and picks a quality preset; Advanced exposes every engine parameter.
2. System validates on every change (frames `4n+1`, supported sizes, divisor, duration ↔ frames).
3. User presses Generate → system builds the recipe and runs the memory guard.
4. System queues a Job; the queue renders one job at a time.
5. Worker reports phases: loading model → encoding prompt → denoising step n/N → decoding → saving.
6. Done → render stored in the Library with its recipe; notification raised.

## Branches and failure paths
- Model not installed → the button reads "Install <model> (<size>)" and opens the Models flow.
- Invalid combination → cannot be queued; the reason sits next to the field (AC-11).
- Memory guard refuses → explanation plus a smaller variant (AC-12).
- Cancel → stops within one denoising step, or the worker is killed after 10 s; memory is freed (AC-20).
- Worker crash → job failed with the last log lines; worker restarted for the next job (AC-21).
- `OOM`, `DISK_FULL` and the other closed error codes → job failed with a plain-language cause.
- App quit while rendering → the app stays in the menu bar; a full quit asks first, and queued jobs
  persist (AC-22).

```mermaid
stateDiagram-v2
  [*] --> queued
  queued --> loading_model
  loading_model --> encoding_prompt --> denoising --> decoding --> saving --> done
  queued --> cancelled
  loading_model --> cancelled
  denoising --> cancelled
  loading_model --> failed
  denoising --> failed
  decoding --> failed
  done --> [*]
  failed --> [*]
  cancelled --> [*]
```
