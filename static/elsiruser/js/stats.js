const renderChart=(data,labels)=>{

  const ctx = document.getElementById('myChart');

const backgroundColors = data.map(() => `rgba(${Math.floor(Math.random() * 255)}, ${Math.floor(Math.random() * 255)}, ${Math.floor(Math.random() * 255)}, 0.2)`);
const borderColors = data.map(() => `rgba(${Math.floor(Math.random() * 255)}, ${Math.floor(Math.random() * 255)}, ${Math.floor(Math.random() * 255)}, 1)`);


new Chart(ctx, {
  type: 'bar',
  data: {
    labels: labels,
    datasets: [{
      label: 'Sales per Service',
      data: data,
      backgroundColor: backgroundColors,
      borderColor: borderColors,
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
           text:'Sales per Service'
       }
       
  }
});

}

const getChartData=()=>{
  fetch('/monthly_servicesales')
  .then(res=>res.json())
  .then(results=>{
      console.log("results",results);
      const services_data = results.services_summary_data
      const [labels,data]=[Object.keys(services_data),Object.values(services_data)]


      renderChart(data, labels);
  });
};

document.onload=getChartData()


