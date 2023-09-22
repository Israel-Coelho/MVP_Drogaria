//Função para obter a lista existente do servidor via requisição GET
const getList = async () => {
  let url = 'http://127.0.0.1:5000/drogarias';
  fetch(url, {
    method: 'get',
  })
    .then((response) => response.json())
    .then((data) => {
      data.drogarias.forEach(item => insertList(item.nome_drogaria, item.nome_responsavel, item.crf,  item.endereco, item.telefone))
    })
    .catch((error) => {
      console.error('Error:', error);
    });
}


//Chamada da função para carregamento inicial dos dados
getList()


//Função para colocar uma drogaria na lista do servidor via requisição POST
const postItem = async (inputCompany, inputContact, inputCrf, inputAddress, inputPhone) => {
  const formData = new FormData();
  formData.append('nome_drogaria', inputCompany);
  formData.append('nome_responsavel', inputContact);
  formData.append('crf', inputCrf);
  formData.append('endereco', inputAddress);
  formData.append('telefone', inputPhone);

  let url = 'http://127.0.0.1:5000/drogaria';
  fetch(url, {
    method: 'post',
    body: formData
  })
    .then((response) => response.json())
    .catch((error) => {
      console.error('Error:', error);
    });
}


//Função para criar um botão close para cada drogaria da lista
const insertButton = (parent) => {
  let span = document.createElement("span");
  let txt = document.createTextNode("\u00D7");
  span.className = "close";
  span.appendChild(txt);
  parent.appendChild(span);
}


//Função para remover uma drogaria da lista de acordo com o click no botão close
const removeElement = () => {
  let close = document.getElementsByClassName("close");
  // var table = document.getElementById('myTable');
  let i;
  for (i = 0; i < close.length; i++) {
    close[i].onclick = function () {
      let div = this.parentElement.parentElement;
      const nomeItem = div.getElementsByTagName('td')[0].innerHTML
      if (confirm("Você tem certeza que deseja remover essa drogaria?")) {
        div.remove()
        deleteItem(nomeItem)
        alert("Removida!")
      }
    }
  }
}


//Função para deletar uma drogaria da lista do servidor via requisição DELETE
const deleteItem = (item) => {
  console.log(item)
  let url = 'http://127.0.0.1:5000/drogaria?nome_drogaria=' + item;
  fetch(url, {
    method: 'delete'
  })
    .then((response) => response.json())
    .catch((error) => {
      console.error('Error:', error);
    });
}


//Função para adicionar uma nova drogaria com nome da drogaria, nome do responsavel, crf (Conselho Regional de Farmácia), endereço e telefone 
const newItem = () => {
  let inputCompany = document.getElementById("newInput").value;
  let inputContact = document.getElementById("newContact").value;
  let inputCrf = document.getElementById("newCrf").value;
  let inputAddress = document.getElementById("newAddress").value;
  let inputPhone = document.getElementById("newPhone").value;
  if (inputCompany === '') {
    alert("Escreva o nome de uma Drogaria!");
  } else {
    insertList(inputCompany, inputContact, inputCrf, inputAddress, inputPhone)
    postItem(inputCompany, inputContact, inputCrf, inputAddress, inputPhone)
    alert("Drogaria adicionada!")
  }
}


//Função para inserir drogaria na lista apresentada
const insertList = (nameCompany, Contact, Crf, Address, Phone) => {
  var item = [nameCompany, Contact, Crf, Address, Phone]
  var table = document.getElementById('myTable');
  var row = table.insertRow();

  for (var i = 0; i < item.length; i++) {
    var cel = row.insertCell(i);
    cel.textContent = item[i];
  }
  insertButton(row.insertCell(-1))
  document.getElementById("newInput").value = "";
  document.getElementById("newContact").value = "";
  document.getElementById("newCrf").value = "";
  document.getElementById("newAddress").value = "";
  document.getElementById("newPhone").value = "";

  removeElement()
}