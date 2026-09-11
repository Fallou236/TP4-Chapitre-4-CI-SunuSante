// Amélioration progressive du formulaire (JS/CSS vanilla, chapitre 2).
//
// Volontairement minimal : on n'y recalcule PAS le tarif (ça ferait une
// 3e copie de la règle métier, en plus de celles à corriger côté Django).
// On se contente d'un avertissement informatif côté client.

document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("form-rdv");
    const dateInput = document.getElementById("date");

    if (!form || !dateInput) {
        return;
    }

    const avertissement = document.createElement("p");
    avertissement.className = "avertissement-weekend";
    avertissement.style.display = "none";
    avertissement.style.color = "#b3261e";
    avertissement.textContent = "Majoration weekend applicable pour cette date.";
    dateInput.insertAdjacentElement("afterend", avertissement);

    dateInput.addEventListener("change", () => {
        const jour = new Date(dateInput.value).getUTCDay(); // 0 = dimanche, 6 = samedi
        avertissement.style.display = jour === 0 || jour === 6 ? "block" : "none";
    });

    // Empêche un double-clic d'envoyer deux fois le même rendez-vous.
    form.addEventListener("submit", () => {
        const bouton = form.querySelector("button[type=submit]");
        if (bouton) {
            bouton.disabled = true;
            bouton.textContent = "Envoi en cours…";
        }
    });
});
