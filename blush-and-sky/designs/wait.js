document.documentElement.classList.add("booting");
Promise.all([
  document.fonts.ready,
  ...Array.from(document.images).map((img) =>
    img.decode ? img.decode().catch(() => {}) : Promise.resolve()
  ),
]).then(() => {
  document.documentElement.classList.add("ready");
});
