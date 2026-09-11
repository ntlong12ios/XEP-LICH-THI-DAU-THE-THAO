const axios = require('axios');
axios.get('http://localhost:8000/categories/4/bracket_slots').then(res => {
   const code = res.data[0].slot_code;
   console.log(code);
   for(let i=0; i<code.length; i++) {
      console.log(code[i], code.charCodeAt(i).toString(16));
   }
});
