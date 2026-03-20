const toggleBtn = document.getElementById("themeToggle");
const htmlElement = document.documentElement;

toggleBtn.addEventListener("click", () => {
    const currentTheme = htmlElement.getAttribute("data-bs-theme");
    const newTheme = currentTheme === "light" ? "dark" : "light";
    htmlElement.setAttribute("data-bs-theme", newTheme);
});