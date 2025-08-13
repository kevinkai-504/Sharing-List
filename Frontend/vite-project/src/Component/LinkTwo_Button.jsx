import { useState } from "react";
import Data_Format from '../Config'




export function LinkTwo_Button({id, id2, type, type2, updateCall, disabled, accesstoken}) {

    const [alreadyLink, setAlreadyLink] = useState(false)



    const url_defalut = Data_Format["url_default"]
    const url = `${url_defalut}/${type}/${id}/${type2}/${id2}`
    const button_color = alreadyLink ? 'btn btn-warning':'btn btn-success'

    const setLink = async() => {
        const options = {
            method: alreadyLink ? 'DELETE':'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${accesstoken}`
            },
        }
        const response = await fetch(url, options)
        if (response.status !== 201 && response.status !== 200) {
            const data = await response.json()
            alert(data.message)
        } else {
            setAlreadyLink(!alreadyLink);
            updateCall();
        }
    }

    const onLink = async() => {
        const options = {
            method: "GET",
            headers: {
                'Authorization': `Bearer ${accesstoken}`
            },
        }
        const response = await fetch(url, options)
        response.status === 200 ? setAlreadyLink(true) : setAlreadyLink(false)
    }
    onLink();

    return (
        <>
            <button disabled={disabled} className={button_color} onClick={() => setLink()}>{alreadyLink ? "刪除標籤":"新增標籤"}</button>
        </>
    )
}



