# Capabilities, access and prerequisites

This is an expectations guide, not an official feature matrix. Capabilities can differ by account, region, connected apps and available environment. Ask dot to check the actual access in your conversation before planning a dependent step.

| Label | What a recipe may ask for | What to verify first | Useful fallback |
| --- | --- | --- | --- |
| `research` | Find sources, compare evidence and write a dated brief | Search or browsing access, source availability and recency | Work from supplied documents and clearly state their date |
| `files` | Inspect or produce documents, spreadsheets and structured files | Supported input, output and a usable download route | Return a draft or a small structured sample |
| `images` | Generate or edit an authorized image | Image tools, reference image access and export format | Prepare an edit brief; do not claim the image was edited |
| `code` | Produce and test code or scripts | A suitable execution environment, dependencies and test access | Deliver code plus explicit unrun checks |
| `websites` | Build an interactive page or browser game | Preview/hosting support and the requested access level | Deliver a local project or prototype specification |
| `connected-apps` | Read or act in an external app | The exact app, account, permissions and supported action | Use a minimal sanitized export supplied by the user |
| `scheduling` | Set a reminder or bounded recurring check | Supported scheduling, personal timezone, delivery destination and stop condition | Provide a calendar-ready plan and say nothing is scheduled |
| `computer-access` | Use files, installed software or apps on a computer | Which computer, whether it is available, and the permitted scope | Work from exported files or supply instructions |

## Three different resources

A conversation with dot does not by itself grant access to your accounts or your computer. A connected app may expose a supported read or action without requiring computer control. A cloud computer and your own computer are separate environments with separate files and software. Ask which environment will be used for a task that depends on local files or installed applications.

## Scheduling is an actual state change

A prompt that describes a recurring task is not proof that the task exists. After setup, verify the timezone, next run, cadence, destination and whether it is enabled. Specify an end date or stopping condition. Event-based triggers and polling are not interchangeable, and availability varies. Avoid promises of continuous, instant or unlimited monitoring.

## 3D and file formats

3D recipes may involve code for tools such as Blender or OpenSCAD if that software is available and appropriate. A script is not a verified model. A rendered image is not a CAD file. Export availability, scale, units, manifold geometry, materials and animation support depend on the toolchain and format. Request the native source, the export format and a verification method separately. Do not rely on study models for construction, electrical safety or load-bearing parts.

## Image editing

Use authorized inputs. Generated or edited images can change fine details, identity cues, lettering and geometry. Verify the final pixels, dimensions, transparency and intended crop. For exact lettering, logos or layout, a layered or vector workflow may be more suitable than an image-generation step. A request for a specific output format still needs verification of the delivered file.

## Sharing and account actions

Describe the destination and intended audience before sharing or publishing. A private draft, a preview link and a public URL are different. Account sign-in, purchases, subscriptions, permissions and protected credentials may require your explicit decision or direct action. A recipe must never instruct you to paste passwords, API keys or full payment details into chat.

## What to ask when something is blocked

“Which exact step is blocked, what access or input is missing, and what useful portion can you finish now?” That is more actionable than asking whether dot can do the whole category in the abstract.
