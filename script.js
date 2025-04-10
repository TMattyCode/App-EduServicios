function buscarPorCodigo() {
    const codigo = document.getElementById("codigoCurso").value.trim();

    if (!codigo) {
        alert("Por favor, ingresa un código de curso.");
        return;
    }

    const soapRequest = `<?xml version="1.0"?>
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                      xmlns:edu="edu.servicios.soap">
        <soapenv:Header/>
        <soapenv:Body>
            <edu:getCursoPorCodigo>
                <codigo>${codigo}</codigo>
            </edu:getCursoPorCodigo>
        </soapenv:Body>
    </soapenv:Envelope>`;

    fetch("http://localhost:8000/soap", {
        method: "POST",
        headers: { "Content-Type": "text/xml" },
        body: soapRequest
    })
    .then(res => res.text())
    .then(xml => {
        const parser = new DOMParser();
        const xmlDoc = parser.parseFromString(xml, "text/xml");
        const result = xmlDoc.getElementsByTagName("getCursoPorCodigoResult")[0]?.textContent;
        document.getElementById("resultadoSoap").textContent = result || "Curso no encontrado";
    })
    .catch(err => {
        console.error("Error SOAP:", err);
        document.getElementById("resultadoSoap").textContent = "Error en la solicitud SOAP.";
    });
}

function listarCursos() {
    fetch("http://localhost:5000/cursos")
        .then(res => res.json())
        .then(data => {
            const lista = document.getElementById("listaCursos");
            lista.innerHTML = "";
            data.forEach(c => {
                const item = document.createElement("li");
                item.textContent = `${c.id} - ${c.codigo} - ${c.nombre}`;
                lista.appendChild(item);
            });
        });
}

function agregarCurso() {
    const codigo = document.getElementById("nuevoCodigo").value;
    const nombre = document.getElementById("nuevoNombre").value;

    fetch("http://localhost:5000/cursos", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ codigo, nombre })
    })
    .then(res => res.json())
    .then(data => alert("Curso agregado: " + data.nombre));
}