import { Delete_Button } from "./Delete_Button";
import { Input_Box } from "./Input_box";
import { useState } from "react";
import { Modal_view } from "./Modal_view";
import { LinkTwo_Button } from "./LinkTwo_Button";

export function Item_List({
  datas,
  attributes,
  updateCall,
  type,
  type2 = "",
  link_id = "",
  link_type = "",
  accesstoken
}) {
  const [isPut, setIsput] = useState(false);
  const [putId, setPutId] = useState("");
  const [openType2, setOpenType2] = useState(false);
  const [type2Id, settype2Id] = useState("");

  const openPut = (target_Id) => {
    setIsput(!isPut);
    setPutId(target_Id);
  };
  const openModal = (target_Id) => {
    setOpenType2(!openType2);
    settype2Id(target_Id);
    console.log(openType2)
  };

  const color_list = {
    A: "table-danger",
    B: "table-warning",
    C: "table-success",
    D: "table-primary",
  };

  return (
    <>
      <div className="container">
        <div className="row row-cols-1 gy-5">
          <div className="col">
            <div className="container">
              <div className="table-responsive">
                <table className="table table-hover table-bordered table-sm">
                  <thead className="table-group-divider">
                    <tr>
                      {attributes.map((attr) => (
                        <th>{attr}</th>
                      ))}
                      <th>操作</th>
                    </tr>
                  </thead>
                  <tbody className="table-group-divider">
                    {datas.toReversed().map((data) => (
                      <tr className={color_list[data["status"]]}>
                        {attributes.map((attr) => (
                          <td>
                            <Input_Box item={data} updateCall={updateCall} type={type} attr={attr} put={isPut && putId === data["id"]} accesstoken={accesstoken}/>
                          </td>
                        ))}
                        <td>
                          <button disabled={isPut && putId !== data["id"]} 
                          className={isPut && putId === data["id"] ? "btn btn-warning" : "btn btn-primary"} onClick={() => openPut(data["id"])}
                          >{isPut && putId === data["id"] ? "收起" : "編輯"}
                          </button>

                          <Delete_Button item={data} updateCall={updateCall} type={type} put={isPut} accesstoken={accesstoken}/>

                          {((type2 !== "")) &&
                            <button disabled={(isPut) || type2 === ""} className="btn btn-success" onClick={() => openModal(data["id"])}>
                              標籤
                            </button>
                          }


                          {(openType2 && type2Id === data["id"]) && (
                            <Modal_view type={type2} link_id={data.id} link_type={type} name={data["name"]} recover={setOpenType2} accesstoken={accesstoken}/>
                          )}

                          {/* Modal裡面打開List時的特有按鈕 */}
                          {(type2 === "") && (
                            <LinkTwo_Button id={link_id} id2={data["id"]} type={link_type} type2={type} updateCall={updateCall} disabled={isPut} accesstoken={accesstoken}/>
                          )}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}
