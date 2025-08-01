import { useState } from "react";
import Data_Format from "../config";

export function Input_Box({item, updateCall, type, attr, put, accesstoken}) {

    const allowChange = Data_Format["learn_allowChange"]
    const IsallowChange = allowChange.indexOf(attr) !== -1
    const attributes = Data_Format["learn"]

    const url_defalut = Data_Format["url_default"]
    const [item_name, setItem_name] = useState(item[attr]);
    const onSubmit = async (e) => {
        e.preventDefault()
        const data = {}
        attributes.map((attribute) => {
            if (allowChange.indexOf(attribute) !== -1) {
                if (attribute !== attr) {
                    data[attribute] = item[attribute]
                } else {
                    data[attr] = item_name
                }
            }
        })

        const url = `${url_defalut}/${type}/${item["id"]}`
        const options = {
            method: "PUT",
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${accesstoken}`
            },
            body: JSON.stringify(data)
        }

        const response = await fetch(url, options)
        if (response.status !== 200) {
            const data = await response.json()
            alert(data.message)
        } else {
            updateCall()
        }
    }
   

    return (
        <>
            <div className="container">
                <form onSubmit={onSubmit}>
                    <div className="input-group">
                        {item[attr]}
                        {(IsallowChange && put) && 
                        <div className="container">
                            <input onChange={(e) => setItem_name(e.target.value)}  type="text"  className="form-control"/>
                            <button className="btn btn-success" type="submit">變更</button>
                        </div>}
                    </div>
                </form>
            </div>
        </>
    )
}



