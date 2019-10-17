function getFilesNames(){
    var fileInput = document.getElementById('validatedCustomFile');
    
    if(fileInput.files.length > 0){
        for(var i = 0; i <= fileInput.files.length - 1; i++){
            document.getElementById('labelFilesLoad') = fileInput.files.item(i).name
        }
    }

}