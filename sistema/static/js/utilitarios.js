function mascaraTelefone() {
    function aplicarMascaraTelefone(valor) {
        valor = valor.replace(/\D/g, ""); // Remove caracteres não numéricos
        valor = valor.replace(/^(\d{2})(\d)/, "($1) $2"); // Adiciona parênteses
        valor = valor.replace(/(\d{5})(\d)/, "$1-$2"); // Adiciona o traço
        return valor.slice(0, 15); // Limite de tamanho
    }

    const inputsTelefone = document.querySelectorAll(".mascara-telefone");

    inputsTelefone.forEach((input) => {
        input.addEventListener('input', (e) => {
            e.target.value = aplicarMascaraTelefone(e.target.value);
        });
    });
}

function validarConfirmarSenha(event) {
    var senha = document.getElementById("senha").value;
    var confirmar_senha = document.getElementById("confirmar_senha").value;

    if (senha !== confirmar_senha) {
        alert("As senhas não coincidem!");
        event.preventDefault();
    }
}

function inicializar() {
    mascaraTelefone();
    document.querySelector("form").addEventListener("submit", validarConfirmarSenha);
}

window.addEventListener('load', inicializar);
