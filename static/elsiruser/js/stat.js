const renderChart=(data,labels)=>{

  const ctx = document.getElementById('myChart2');

new Chart(ctx, {
  type: 'line',
  data: {
    labels: ['Jan', 'Feb','Mar','Apr','May','Jun','Jul','Aug','Sept','Oct','Nov','Dec'],
    datasets: [{
      label: 'Sales',
      data: data,
      borderWidth: 1
    }]
  },
  options: {
    scales: {
      y: {
        beginAtZero: true
      }
    },
       title:{
           display:true,
           text:'Monthly sales distribution'
       }
       
  }
});

}

const getChartData=()=>{
  fetch('/monthly_sales_distribution')
  .then(res=>res.json())
  .then(results=>{
      console.log("results",results);
      const services_data = results.services_summary_data
      const [labels,data]=[Object.keys(services_data),Object.values(services_data)]


      renderChart(data, labels);
  });
};

document.onload=getChartData()


