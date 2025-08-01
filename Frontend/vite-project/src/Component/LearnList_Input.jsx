import {useState } from "react";
import Data_Format from "../config";

export function LearnList_Input({updateCall, type, accesstoken}) {

    const url_defalut = Data_Format["url_default"]

    // 手動更改(1/3)
    const [learning_name, setLearning_name] = useState("");
    const [learning_note, setLearning_note] = useState("");

    const onSubmit = async (e) => {
        e.preventDefault()

        // 手動更改(2/3)
        const data = {
            "name":learning_name,
            "note":learning_note,
        }

        
        const options = {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${accesstoken}`
            },
            body: JSON.stringify(data)
        }

        const url = `${url_defalut}/${type}`
        const response = await fetch(url, options)
        if (response.status !== 201) {
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
                    <label className="form-label">建立項目</label>
                    <div className="input-group">
                        {/* // 手動更改(3/3) */}
                        <input onChange={(e) => setLearning_name(e.target.value)}  type="text" required className="form-control learn" placeholder="name:內容" />
                        <input onChange={(e) => setLearning_note(e.target.value)}  type="text" className="form-control learn" placeholder="(選填)note:筆記"/>
                    </div>
                    <button className="btn btn-info" type="submit">新增</button>
                </form>
            </div>
        </>
    )
}



