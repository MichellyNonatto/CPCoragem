'use strict';
const exibirErro = (message) => {
    const errorMessage = document.getElementById('error-message');
    errorMessage.textContent = message;
}

const limparErro = () => {
    exibirErro('');
}
const preencherFormulario = (endereco) => {
    limparErro();
    const ruas = document.querySelectorAll('[name="rua"]');
    const bairros = document.querySelectorAll('[name="bairro"]');
    const cidades = document.querySelectorAll('[name="cidade"]');
    const estados = document.querySelectorAll('[name="estado"]');

    Array.from(ruas).forEach(element => {
        element.value = endereco.logradouro || "";
    });

    Array.from(bairros).forEach(element => {
        element.value = endereco.bairro || "";
    });

    Array.from(cidades).forEach(element => {
        element.value = endereco.localidade || "";
    });

    Array.from(estados).forEach(element => {
        element.value = endereco.uf || "";
    });
}

const pesquisarCep = async () => {
    const cep = document.getElementById('id_cep').value;

    if (!cep || cep.length !== 8) {
        exibirErro("Por favor, informe um CEP válido.");
        return;
    }

    const url = `http://viacep.com.br/ws/${cep}/json/`;

    try {
        const resposta = await fetch(url);

        if (!resposta.ok) {
            exibirErro("Erro na requisição: " + resposta.status);
            return;
        }

        const endereco = await resposta.json();
        if (endereco.erro) {
            exibirErro("Por favor, informe um CEP válido.");
            return;
        }
        preencherFormulario(endereco);
    } catch (erro) {
        exibirErro('Erro na requisição: ' + erro.message);
    }
}

document.getElementById('id_cep').addEventListener('focusout', pesquisarCep);
