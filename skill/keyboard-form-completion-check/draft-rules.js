/* Original fictional fixture. Pure business rules shared by both page revisions. */
const DraftRules = Object.freeze({
  validate(values) {
    const errors = [];
    const code = values.code.trim();
    const kitsText = values.kits.trim();
    const kits = Number(kitsText);
    if (!/^LANTERN-[0-9]{2}$/.test(code)) {
      errors.push({ field: "code", message: "Workshop code: enter LANTERN- followed by two digits, for example LANTERN-42." });
    }
    if (!/^[1-4]$/.test(kitsText)) {
      errors.push({ field: "kits", message: "Number of kits: enter a whole number from 1 to 4." });
    }
    if (!["North shelf", "West shelf"].includes(values.shelf)) {
      errors.push({ field: "shelf", message: "Pickup shelf: choose North shelf or West shelf." });
    }
    return { errors, draft: errors.length ? null : { code, kits, shelf: values.shelf } };
  },
  describe(draft) {
    return `Local draft ready: ${draft.code}; ${draft.kits} ${draft.kits === 1 ? "kit" : "kits"}; ${draft.shelf}. Nothing has been sent or reserved.`;
  }
});
