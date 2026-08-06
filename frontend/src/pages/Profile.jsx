import { useEffect, useState } from "react";
import { API } from "../api/api";

export function Profile(){
    const [user,setUser] = useState(null);

    useEffect(()=>{

        const getProfile = async()=>{

            try{
                const token = localStorage.getItem("access_token");
                const response = await API.get(
                    "/users/me",
                    {
                        headers:{
                            Authorization:
                            `Bearer ${token}`
                        }
                    }
                );

                setUser(response.data);

            }catch(error){
                console.log(error.response?.data);
            }
        };
        
        getProfile();
        
    },[]);

    if(!user){
        return <h1>Loading...</h1>
    }

    return(
        <div>
            <h1>
                Profile
            </h1>

            <p>
                ID: {user.id}
            </p>

            <p>
                Username: {user.username}
            </p>

            <p>
                Email: {user.email}
            </p>
        </div>
    )
}
