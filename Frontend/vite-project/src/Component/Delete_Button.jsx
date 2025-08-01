import Data_Format from "../config"

export function Delete_Button({item, updateCall, type, put, accesstoken}) {
    const url_default = Data_Format["url_default"]
    const onDelete = async () => {
        const options = {
            method: "DELETE",
            headers: {
                'Authorization': `Bearer ${accesstoken}`
            },
        }
       
        const response = await fetch(`${url_default}/${type}/${item["id"]}`, options)
        if (response.status !== 200) {
            const data = await response.json()
            alert(data.message)
        } else {
            updateCall()
        }
    }

    return (
        <>
            <button disabled={put} className="btn btn-danger" onClick={() => onDelete()}>刪除</button>
        </>
    )
}
