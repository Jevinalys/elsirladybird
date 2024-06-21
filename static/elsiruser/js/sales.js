var db = indexedDB.open('db.sqlite3',1); 


(function ($){

    $('#serviceID').change(function(){
        db.transaction(function(transaction){
            var sql= "SELECT * FROM Service";
            transaction.executeSql(sql,undefined,
                function(transaction,result){

                    console.log(result.service_price) 

                }
            )
        })

    })

})






/*function selectPrice() {
  let service = document.getElementById("serviceID").value

  console.log(service);
};*/
