import { useState } from "react";
import Data_Format from '../Config'

export function TagList_Input({updateCall, type, accesstoken}) {

    const url_defalut = Data_Format["url_default"]

    // 手動更改(1/3)
    const [tag_name, setTag_name] = useState("")

    const onSubmit = async (e) => {
        e.preventDefault()

        // 手動更改(2/3)
        const data = {
            "name":tag_name,
        }

        const url = `${url_defalut}/${type}`
        const options = {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                'Authorization': `Bearer ${accesstoken}`
            },
            body: JSON.stringify(data)
        }

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
                    <label className="form-label">建立標籤</label>
                    <div className="input-group">
                        {/* // 手動更改(3/3) */}
                        <input onChange={(e) => setTag_name(e.target.value)}  type="text" required className="form-control learn" placeholder="name:標籤名稱" />
                    </div>
                    <button className="btn btn-info" type="submit">新增</button>
                </form>
            </div>
        </>
    )
}



