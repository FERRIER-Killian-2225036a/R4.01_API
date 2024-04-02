import uvicorn
from core.config import HOST, PORT
from API_controller.General_Controller import General_Controller
from data_access.Data import Data

if __name__ == "__main__":
    data = Data()
    controller = General_Controller(data)
    controller.setup_routes()
    controller.data_transmission()
    uvicorn.run(controller.getApp(), host=HOST, port=PORT)
