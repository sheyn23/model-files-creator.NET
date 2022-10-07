import os

# Получение названия проекта
projectName = input("Введите название проекта: ")

# Получение названия модели
modelName = input("Введите название модели в стиле CamelCase: ")

# Получение настоящей директории
currentDir = os.path.dirname(os.path.realpath(__file__))
print(f"Файлы будут созданы в директории: {currentDir}")

controllerContent = (f"using AutoMapper;\n"
                     f"using Microsoft.AspNetCore.Authorization;\n"
                     f"using Microsoft.AspNetCore.Mvc;\n"
                     f"using Microsoft.Extensions.Logging;\n"
                     f"using {projectName}.Core.Entities;\n"
                     f"using {projectName}.Core.Models.Dto.{modelName};\n"
                     f"using {projectName}.Core.Models.Request;\n"
                     f"using {projectName}.Core.Models.Response;\n"
                     f"using {projectName}.Core.Repository;\n"
                     f"using System;\n"
                     f"using System.Collections.Generic;\n"
                     f"using System.Threading.Tasks;\n"
                     f"\n"
                     f"namespace {projectName}.Api.Controllers\n"
                     f"{{\n"
                     f"    [Produces(\"application/json\")]\n"
                     f"    [Route(\"api/v{{v:apiVersion}}/{modelName.lower()}\")]\n"
                     f"    [ApiController, ApiVersion(\"1\")]\n"
                     f"    public class {modelName}Controller : ControllerBase\n"
                     f"    {{\n"
                     f"        private readonly IMapper _mapper;\n"
                     f"        private readonly I{modelName}Service _{modelName.lower()}Service;\n"
                     f"        private readonly ILogger _logger;\n"
                     f"        public {modelName}Controller(IMapper mapper, I{modelName}Service {modelName.lower()}Service, ILogger<{modelName}Controller> logger)\n"
                     f"        {{\n"
                     f"            _mapper = mapper;\n"
                     f"            _{modelName.lower()}Service = {modelName.lower()}Service;\n"
                     f"            _logger = logger;\n"
                     f"        }}\n"
                     f"\n"
                     f"        [HttpPost(\"get/{{id}}\")]\n"
                     f"        public async Task<ResultRequest<Dto{modelName}>> GetAsync(Guid? id)\n"
                     f"        {{\n"
                     f"            try\n"
                     f"            {{\n"
                     f"                if (id == null) return ResultRequest<Dto{modelName}>.Error(\"{modelName} request fail\", \"Invalid request data\");\n"
                     f"\n"
                     f"                var {modelName.lower()} = await _{modelName.lower()}Service.GetAsync<{modelName}>((Guid)id);\n"
                     f"                return ResultRequest<Dto{modelName}>.Ok(_mapper.Map<Dto{modelName}>({modelName.lower()}));\n"
                     f"            }}\n"
                     f"            catch (Exception e)\n"
                     f"            {{\n"
                     f"                return ResultRequest<Dto{modelName}>.Error(\"Request {modelName} error\", e.Message);\n"
                     f"            }}\n"
                     f"        }}\n"
                     f"\n"
                     f"        [HttpPost(\"get-all\")]\n"
                     f"        public async Task<ResultRequest<List<Dto{modelName}>>> GetAllAsync()\n"
                     f"        {{\n"
                     f"            try\n"
                     f"            {{\n"
                     f"                var {modelName.lower()} = await _{modelName.lower()}Service.GetAllAsync<{modelName}>();\n"
                     f"                return ResultRequest<List<Dto{modelName}>>.Ok(_mapper.Map<List<Dto{modelName}>>({modelName.lower()}));\n"
                     f"            }}\n"
                     f"            catch (Exception e)\n"
                     f"            {{\n"
                     f"                return ResultRequest<List<Dto{modelName}>>.Error(\"Get All {modelName.lower()} error\", e.Message);\n"
                     f"            }}\n"
                     f"        }}\n"
                     f"\n"
                     f"        [HttpPost(\"update\")]\n"
                     f"        public async Task<ResultRequest> UpdateAsync([FromBody] InboundRequest<Dto{modelName}> request)\n"
                     f"        {{\n"
                     f"            try\n"
                     f"            {{\n"
                     f"                var dto = request?.Data;\n"
                     f"\n"
                     f"                if (dto == null)\n"
                     f"                {{\n"
                     f"                    return ResultRequest.Error(\"Error\", \"Invalid {modelName.lower()} request data\");\n"
                     f"                }}\n"
                     f"\n"
                     f"                var {modelName.lower()} = await _{modelName.lower()}Service.GetAsync<{modelName}>((Guid)dto.Id);\n"
                     f"                \n"
                     f"                if ({modelName.lower()} == null)\n"
                     f"                {{\n"
                     f"                    return ResultRequest.Error(\"Error\", \"Wrong {modelName.lower()} id\");\n"
                     f"                }}\n"
                     f"                \n"
                     f"                _mapper.Map(dto, {modelName.lower()});\n"
                     f"                _{modelName.lower()}Service.Update({modelName.lower()});\n"
                     f"                return ResultRequest.Ok();\n"
                     f"            }}\n"
                     f"            catch (Exception e)\n"
                     f"            {{\n"
                     f"                return ResultRequest.Error(\"Error\", e.ToString());\n"
                     f"            }}\n"
                     f"        }}\n"
                     f"\n"
                     f"        [HttpPost(\"add\")]\n"
                     f"        public async Task<ResultRequest<Dto{modelName}>> AddAsync([FromBody] InboundRequest<Dto{modelName}> request)\n"
                     f"        {{\n"
                     f"            try\n"
                     f"            {{\n"
                     f"                var dto = request?.Data;\n"
                     f"\n"
                     f"                if (dto == null)\n"
                     f"                {{\n"
                     f"                    return ResultRequest<Dto{modelName}>.Error(\"Add {modelName.lower()} error\", \"Invalid request data\");\n"
                     f"                }}\n"
                     f"\n"
                     f"                dto.Id = Guid.NewGuid();\n"
                     f"                var tag{modelName} = _mapper.Map<{modelName}>(dto);\n"
                     f"                var added{modelName} = await _{modelName.lower()}Service.AddAsync<{modelName}>(tag{modelName});\n"
                     f"                var mapped{modelName} = _mapper.Map<Dto{modelName}>(added{modelName});\n"
                     f"                return ResultRequest<Dto{modelName}>.Ok(mapped{modelName});\n"
                     f"            }}\n"
                     f"            catch (Exception e)\n"
                     f"            {{\n"
                     f"                return ResultRequest<Dto{modelName}>.Error(\"Adding {modelName.lower()} error\", e.Message);\n"
                     f"            }}\n"
                     f"        }}\n"
                     f"\n"
                     f"        [HttpPost(\"delete/{{id}}\")]\n"
                     f"        public ResultRequest Delete(Guid? id)\n"
                     f"        {{\n"
                     f"            try\n"
                     f"            {{\n"
                     f"                _{modelName.lower()}Service.Delete<{modelName}>((Guid)id);\n"
                     f"                return ResultRequest.Ok();\n"
                     f"            }}\n"
                     f"            catch (Exception e)\n"
                     f"            {{\n"
                     f"                return ResultRequest.Error(\"Deleting element error\", e.Message);\n"
                     f"            }}\n"
                     f"        }}\n"
                     f"    }}\n"
                     f"}}\n")
serviceContent = (f"using {projectName}.Core.RepositoryInterfaces;\n"
                  f"using {projectName}.Core.ServiceInterfaces;\n"
                  f"\n"
                  f"namespace {projectName}.BLL.Services\n"
                  f"{{\n"
                  f"    public class {modelName}Service : ServiceBase, I{modelName}Service\n"
                  f"    {{\n"
                  f"        private readonly IUnitOfWork _unitOfWork;\n"
                  f"\n"
                  f"        public {modelName}Service(IUnitOfWork unitOfWork) : base(unitOfWork)\n"
                  f"        {{\n"
                  f"            _unitOfWork = unitOfWork;\n"
                  f"        }}\n"
                  f"    }}\n"
                  f"}}\n")
dtoContent = (f"using Newtonsoft.Json;\n"
              f"using {projectName}.Core.Models.Dto;\n"
              f"using System;\n"
              f"using System.Collections.Generic;\n"
              f"\n"
              f"namespace {projectName}.Core.Models.Dto.{modelName}\n"
              f"{{\n"
              f"    public class Dto{modelName}\n"
              f"    {{\n"
              f"        [JsonProperty(PropertyName = \"id\")]\n"
              f"        public Guid Id {{ get; set; }}\n"
              f"\n"
              f"        [JsonProperty(PropertyName = \"name\")]\n"
              f"        public string Name {{ get; set; }}\n"
              f"    }}\n"
              f"}}\n")
iRepoContent = (f"using {projectName}.Core.Entities;\n"
                f"using System;\n"
                f"using System.Threading.Tasks;\n"
                f"\n"
                f"namespace {projectName}.Core.RepositoryInterfaces\n"
                f"{{\n"
                f"    public interface I{modelName}Repository  : IRepository<{modelName}>\n"
                f"    {{\n"
                f"    }}\n"
                f"}}\n")
iServiceContent = (f"using System;\n"
                   f"using System.Threading.Tasks;\n"
                   f"using {projectName}.Core.Entities;\n"
                   f"using {projectName}.Core.OperationInterfaces;\n"
                   f"\n"
                   f"namespace {projectName}.Core.ServiceInterfaces\n"
                   f"{{\n"
                   f"    public interface I{modelName}Service : IServiceBase\n"
                   f"    {{\n"
                   f"    }}\n"
                   f"}}\n")
repoContent = (f"using {projectName}.Core.RepositoryInterfaces;\n"
               f"using {projectName}.Core.Entities;\n"
               f"using System;\n"
               f"using System.Collections.Generic;\n"
               f"using Microsoft.EntityFrameworkCore;\n"
               f"using System.Threading.Tasks;\n"
               f"\n"
               f"namespace {projectName}.DAL.Repositories\n"
               f"{{\n"
               f"    public class {modelName}Repository : Repository<{modelName}>, I{modelName}Repository\n"
               f"    {{\n"
               f"        public {modelName}Repository({projectName}DbContext context) : base(context)\n"
               f"        {{\n"
               f"        }}\n"
               f"        public {projectName}DbContext {projectName}DbContext => Context as {projectName}DbContext;\n"
               f"    }}\n"
               f"}}\n"
               )


def yes_no_dialog(question, default_answer="yes"):
    answers = {"yes": 1, "y": 1, "ye": 1,
               "no": 0, "n": 0}
    if default_answer == None:
        tip = " [y/n] "
    elif default_answer == "yes":
        tip = " [Y/n] "
    elif default_answer == "no":
        tip = " [y/N] "
    else:
        raise ValueError(f'Неверное значение: {default_answer = }')
    while True:
        print(question + tip + ": ", end="")
        user_answer = input().lower()
        if default_answer is not None and user_answer == '':
            return answers[default_answer]
        elif user_answer in answers:
            return answers[user_answer]
        else:
            print("Пожалуйста, введите yes/y или no/n\n")


def createFile(path, name, content):
    currentPath = currentDir + f"{path}"
    folderExist = os.path.exists(currentPath)

    if not folderExist:
        # Создать папку .DAL/Repositories
        os.makedirs(currentPath)
        print(f"{path} директория создана!")

    with open(f"{currentPath}/{name}", "w") as file:
        file.write(content)


# createFolderAsk = yes_no_dialog(
#     f"Создать папку {projectName}.Api/Controllers", "no")
# print("результат опроса", createFolderAsk)

createFile(
    f"/{projectName}.Api/Controllers",
    f"{modelName}Controller.cs",
    controllerContent
)

createFile(
    f"/{projectName}.BLL/Services",
    f"{modelName}Service.cs",
    serviceContent
)

createFile(
    f"/{projectName}.Core/Models/Dto/{modelName}",
    f"/Dto{modelName}.cs",
    dtoContent
)

createFile(
    f"/{projectName}.Core/RepositoryInterfaces",
    f"/I{modelName}Repository.cs",
    iRepoContent
)

createFile(
    f"/{projectName}.Core/ServiceInterfaces",
    f"/I{modelName}Service.cs",
    iServiceContent
)

createFile(
    f"/{projectName}.DAL/Repositories",
    f"/{modelName}Repository.cs",
    repoContent
)
