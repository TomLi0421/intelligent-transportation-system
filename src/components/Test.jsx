import React, { useEffect } from 'react'
import axios from 'axios'

function Test() {
    useEffect(() => {
        axios.post('http://localhost:8080/getdata')
            .then(res => {
                console.log(res.data);
            })
            .catch(err => console.log(err));
        
    },[])
  return (
    <div style={{backgroundColor:"red"}}>
        Tesing Div
    </div>
  )
}

export default Test