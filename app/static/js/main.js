function getFilesNames(){

    console.log("Entra a funcion para obtener los nombres de los archivos")

    var fileInput = document.getElementById('validatedCustomFile');
    var loadFiles = fileInput.files;
    var file;
    var fileList;

    if(loadFiles.length > 0){
        console.log("Entra a if de la funcion")
        for(var i = 0; i < loadFiles.length; i++){
            file = loadFiles[i].name;
            console.log("Nombre del archivo: [" + file + "]");
            fileList = fileList + "," + file;
        }

        console.log("Se muestran los nombres de los archivos")
        document.getElementById('labelFilesLoad') = fileList;
        alert(fileList);
    }

}