#!/usr/bin/env python3.9.6
import os
from pathlib import Path


class ChangeParams():
    def __init__(self, where, what):
        self.whereChange = where
        self.whatChange = what


class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# Получение названия проекта
projectName = input("Введите название проекта: ")

# Получение названия модели
modelName = input("Введите название модели в стиле CamelCase: ")

# Получение настоящей директории
currentDir = os.path.dirname(os.path.realpath(__file__))
print(f"Файлы будут созданы в директории: {currentDir}")

# Содержимое файлов модели
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
                     f"using System.Threading.Tasks;\n\n"

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
                     f"        }}\n\n"

                     f"        [HttpPost(\"get/{{id}}\")]\n"
                     f"        public async Task<ResultRequest<Dto{modelName}>> GetAsync(Guid? id)\n"
                     f"        {{\n"
                     f"            try\n"
                     f"            {{\n"
                     f"                if (id == null) return ResultRequest<Dto{modelName}>.Error(\"{modelName} request fail\", \"Invalid request data\");\n\n"
                     f"                var {modelName.lower()} = await _{modelName.lower()}Service.GetAsync<{modelName}>((Guid)id);\n"
                     f"                return ResultRequest<Dto{modelName}>.Ok(_mapper.Map<Dto{modelName}>({modelName.lower()}));\n"
                     f"            }}\n"
                     f"            catch (Exception e)\n"
                     f"            {{\n"
                     f"                return ResultRequest<Dto{modelName}>.Error(\"Request {modelName} error\", e.Message);\n"
                     f"            }}\n"
                     f"        }}\n\n"
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
                     f"        }}\n\n"
                     f"        [HttpPost(\"update\")]\n"
                     f"        public async Task<ResultRequest> UpdateAsync([FromBody] InboundRequest<Dto{modelName}> request)\n"
                     f"        {{\n"
                     f"            try\n"
                     f"            {{\n"
                     f"                var dto = request?.Data;\n\n"
                     f"                if (dto == null)\n"
                     f"                {{\n"
                     f"                    return ResultRequest.Error(\"Error\", \"Invalid {modelName.lower()} request data\");\n"
                     f"                }}\n\n"
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
                     f"        }}\n\n"
                     f"        [HttpPost(\"add\")]\n"
                     f"        public async Task<ResultRequest<Dto{modelName}>> AddAsync([FromBody] InboundRequest<Dto{modelName}> request)\n"
                     f"        {{\n"
                     f"            try\n"
                     f"            {{\n"
                     f"                var dto = request?.Data;\n\n"
                     f"                if (dto == null)\n"
                     f"                {{\n"
                     f"                    return ResultRequest<Dto{modelName}>.Error(\"Add {modelName.lower()} error\", \"Invalid request data\");\n"
                     f"                }}\n\n"
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
                     f"        }}\n\n"
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
                  f"using {projectName}.Core.ServiceInterfaces;\n\n"

                  f"namespace {projectName}.BLL.Services\n"
                  f"{{\n"
                  f"    public class {modelName}Service : ServiceBase, I{modelName}Service\n"
                  f"    {{\n"
                  f"        private readonly IUnitOfWork _unitOfWork;\n\n"

                  f"        public {modelName}Service(IUnitOfWork unitOfWork) : base(unitOfWork)\n"
                  f"        {{\n"
                  f"            _unitOfWork = unitOfWork;\n"
                  f"        }}\n"
                  f"    }}\n"
                  f"}}\n")

dtoContent = (f"using Newtonsoft.Json;\n"
              f"using {projectName}.Core.Models.Dto;\n"
              f"using System;\n"
              f"using System.Collections.Generic;\n\n"

              f"namespace {projectName}.Core.Models.Dto.{modelName}\n"
              f"{{\n"
              f"    public class Dto{modelName}\n"
              f"    {{\n"
              f"        [JsonProperty(PropertyName = \"id\")]\n"
              f"        public Guid Id {{ get; set; }}\n\n"

              f"        [JsonProperty(PropertyName = \"name\")]\n"
              f"        public string Name {{ get; set; }}\n"
              f"    }}\n"
              f"}}\n")

iRepoContent = (f"using {projectName}.Core.Entities;\n"
                f"using System;\n"
                f"using System.Threading.Tasks;\n\n"

                f"namespace {projectName}.Core.RepositoryInterfaces\n"
                f"{{\n"
                f"    public interface I{modelName}Repository  : IRepository<{modelName}>\n"
                f"    {{\n"
                f"    }}\n"
                f"}}\n")

iServiceContent = (f"using System;\n"
                   f"using System.Threading.Tasks;\n"
                   f"using {projectName}.Core.Entities;\n"
                   f"using {projectName}.Core.OperationInterfaces;\n\n"
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
               f"using System.Threading.Tasks;\n\n"
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

# Содержимое файлов для декларации
mapProfileContent = (
    f"using AutoMapper;\n"
    f"using Microsoft.Extensions.Configuration;\n"
    f"using {projectName}.Core.Entities;\n"
    f"using {projectName}.Core.Models.Dto.{modelName};\n"
    f"using NetTopologySuite.Geometries;\n\n"
    f"namespace {projectName}.Api\n"
    f"{{\n"
    f"    internal class MapProfile : Profile\n"
    f"    {{\n"
    f"        public MapProfile(IConfiguration configuration)\n"
    f"        {{\n"
    f"			Configure{modelName}();\n"
    f"        }}\n"
    f"		private void Configure{modelName}()\n"
    f"		{{\n"
    f"		    CreateMap<{modelName}, Dto{modelName}>();\n"
    f"		    CreateMap<Dto{modelName}, {modelName}>();\n"
    f"		}}\n"
    f"    }}\n"
    f"}}\n"
)


startupContent = (
    f"using AutoMapper;\n"
    f"using Microsoft.AspNetCore.Builder;\n"
    f"using Microsoft.AspNetCore.Hosting;\n"
    f"using Microsoft.AspNetCore.Mvc;\n"
    f"using Microsoft.EntityFrameworkCore;\n"
    f"using Microsoft.Extensions.Configuration;\n"
    f"using Microsoft.Extensions.DependencyInjection;\n"
    f"using Microsoft.Extensions.Hosting;\n"
    f"using Microsoft.Extensions.Logging;\n"
    f"using Microsoft.Net.Http.Headers;\n"
    f"using Microsoft.OpenApi.Models;\n"
    f"using {projectName}.Api.Extensions;\n"
    f"using {projectName}.Api.Hubs;\n"
    f"using {projectName}.BLL.Services;\n"
    f"using {projectName}.Core.Entities;\n"
    f"using {projectName}.Core.Helpers;\n"
    f"using {projectName}.Core.Models.Auth;\n"
    f"using {projectName}.Core.OperationInterfaces;\n"
    f"using {projectName}.Core.RepositoryInterfaces;\n"
    f"using {projectName}.Core.ServiceInterfaces;\n"
    f"using {projectName}.DAL;\n"
    f"using {projectName}.DAL.Repositories;\n"
    f"using Swashbuckle.AspNetCore.SwaggerGen;\n"
    f"using System.Linq;\n"
    f"using System.Reflection;\n\n"
    f"namespace {projectName}.Api\n"
    f"{{\n"
    f"    public class Startup\n"
    f"    {{\n"
    f"        public Startup(IConfiguration configuration)\n"
    f"        {{\n"
    f"            Configuration = configuration;\n"
    f"        }}\n\n"
    f"        public IConfiguration Configuration {{ get; }}\n"
    f"        public void ConfigureServices(IServiceCollection services)\n"
    f"        {{\n"
    f"            services.AddSingleton(provider =>\n"
    f"                                         new MapperConfiguration(expression => expression.AddProfile(new MapProfile(Configuration))).CreateMapper());\n"
    f"            var tokenAuthConfiguration = Configuration.GetSection(\"TokenAuthentication\").Get<TokenAuthenticationConfiguration>();\n\n"
    f"            services.AddAuth(tokenAuthConfiguration, AuthenticationValidation.GetIdentityByLoginPair, AuthenticationValidation.GetIdentityByApiKey);\n\n"
    f"            services.AddDbContext<{projectName}DbContext>(options =>\n"
    f"            {{\n"
    f"                options.UseNpgsql(Configuration.GetConnectionString(\"DBConnectionString\"), o => o.UseNetTopologySuite());\n"
    f"            }});\n"
    f"            services.AddCors(options =>\n"
    f"            {{\n"
    f"                options.AddPolicy(\"CorsPolicy\",\n"
    f"                    builder => builder.WithOrigins(\n"
    f"                        \"http://127.0.0.1:4200\",\n"
    f"                        \"http://localhost:4200\",\n"
    f"                        \"http://{projectName.lower()}.primorsky.ru\",\n"
    f"                        \"http://{projectName.lower()}-api.primorsky.ru\",\n"
    f"                        \"https://{projectName.lower()}.primorsky.ru\",\n"
    f"                        \"https://{projectName.lower()}-api.primorsky.ru\"\n"
    f"                    )\n"
    f"                    .AllowAnyMethod()\n"
    f"                    .AllowAnyHeader()\n"
    f"                    .AllowCredentials());\n"
    f"            }});\n"
    f"            services.AddSignalR();\n"
    f"            services.AddControllers();\n"
    f"            services.AddApiVersioning();\n"
    f"            services.AddSwaggerGen(c =>\n"
    f"            {{\n"
    f"                c.SwaggerDoc(\"v1\", new OpenApiInfo\n"
    f"                {{\n"
    f"                    Title = \"{projectName} API\",\n"
    f"                    Version = \"v1\"\n"
    f"                }});\n"
    f"                c.DocInclusionPredicate((docName, apiDesc) =>\n"
    f"                {{\n"
    f"                    if (!apiDesc.TryGetMethodInfo(out MethodInfo methodInfo)) return false;\n\n"
    f"                    var versions = methodInfo.DeclaringType\n"
    f"                        .GetCustomAttributes(true)\n"
    f"                        .OfType<ApiVersionAttribute>()\n"
    f"                        .SelectMany(attr => attr.Versions);\n\n"
    f"                    return versions.Any(v => $\"v{{v}}\" == docName);\n"
    f"                }});\n"
    f"                c.AddSecurityDefinition(\"Bearer\", new OpenApiSecurityScheme\n"
    f"                {{\n"
    f"                    In = ParameterLocation.Header,\n"
    f"                    Description = \"Please insert JWT with Bearer into field\",\n"
    f"                    Name = \"Authorization\",\n"
    f"                    Type = SecuritySchemeType.ApiKey\n"
    f"                }});\n"
    f"                c.AddSecurityRequirement(new OpenApiSecurityRequirement {{\n"
    f"                   {{\n"
    f"                     new OpenApiSecurityScheme\n"
    f"                     {{\n"
    f"                       Reference = new OpenApiReference\n"
    f"                       {{\n"
    f"                         Type = ReferenceType.SecurityScheme,\n"
    f"                         Id = \"Bearer\"\n"
    f"                       }}\n"
    f"                      }},\n"
    f"                      System.Array.Empty<string>()\n"
    f"                    }}\n"
    f"                  }});\n"
    f"            }});\n"
    f"            \n"
    f"            ConfigureEnvServices(services);\n"
    f"        }}\n\n"
    f"        public void Configure(IApplicationBuilder app, IWebHostEnvironment env, ILoggerFactory loggerFactory)\n"
    f"        {{\n"
    f"            if (env.IsDevelopment())\n"
    f"            {{\n"
    f"                app.UseDeveloperExceptionPage();\n"
    f"            }}\n"
    f"            else\n"
    f"            {{\n"
    f"                app.UseHsts();\n"
    f"            }}\n\n"
    f"            app.UseStaticFiles();\n"
    f"            app.UseSwagger();\n"
    f"            app.UseSwaggerUI(c =>\n"
    f"            {{\n"
    f"                c.SwaggerEndpoint(\"/swagger/v1/swagger.json\", \"My API V1\");\n"
    f"            }});\n"
    f"            app.UseRouting();\n"
    f"            app.UseCors(\"CorsPolicy\");\n"
    f"            app.UseAuthentication();\n"
    f"            app.UseAuthorization();\n"
    f"            app.UseEndpoints(endpoints =>\n"
    f"            {{\n"
    f"                endpoints.MapHub<MessageHub>(\"/message-hub\");\n"
    f"                endpoints.EnableDependencyInjection();\n"
    f"                endpoints.Select().Filter().Expand();\n"
    f"                endpoints.MapControllers();\n"
    f"            }});\n"
    f"        }}\n"
    f"        public void ConfigureEnvServices(IServiceCollection services)\n"
    f"        {{\n"
    f"			services.AddScoped<I{modelName}Service>(provider =>\n"
    f"				new {modelName}Service(provider.GetService<IUnitOfWork>()));\n"
    f"        }}\n"
    f"    }}\n"
    f"}}\n"
)


iUnitOfWorkContent = (
    f"using Microsoft.EntityFrameworkCore.Storage\n;"
    f"using System\n;"
    f"using System.Collections.Generic\n;"
    f"using System.Threading.Tasks\n\n;"
    f"namespace {projectName}.Core.RepositoryInterfaces\n"
    f"{{\n"
    f"    public interface IUnitOfWork: IDisposable\n"
    f"    {{\n"
    f"        IRepository<T> Repository<T>()\n"
    f"          where T: class;\n\n"
    f"        I{modelName}Repository {modelName}s {{ get; }}\n\n"
    f"        IDbContextTransaction BeginTransaction();\n"
    f"        int ExecuteSqlCommand(FormattableString _sql);\n"
    f"        Task<int> ExecuteSqlCommandAsync(FormattableString _sql);\n"
    f"        int ExecuteSqlCommand(string sql);\n"
    f"        Task<int> ExecuteSqlCommandAsync(string sql);\n"
    f"        IEnumerable<dynamic> GetObjectsToSQL(string sql);\n"
    f"        Task<IEnumerable<dynamic>> GetObjectsToSQLAsync(string sql);\n"
    f"        int Complete();\n"
    f"    }}\n"
    f"}}\n"
)


unitOfWorkContent = (
    f"using Microsoft.EntityFrameworkCore;\n"
    f"using Microsoft.EntityFrameworkCore.Storage;\n"
    f"using {projectName}.Core.Entities;\n"
    f"using {projectName}.Core.RepositoryInterfaces;\n"
    f"using System;\n"
    f"using System.Collections.Generic;\n"
    f"using System.Data;\n"
    f"using System.Data.Common;\n"
    f"using System.Dynamic;\n"
    f"using System.Threading.Tasks;\n\n"
    f"namespace {projectName}.DAL.Repositories\n"
    f"{{\n"
    f"    public class UnitOfWork : IUnitOfWork\n"
    f"    {{\n"
    f"        public readonly {projectName}DbContext _context;\n\n"
    f"        public IUserRepository Users {{ get; }}\n"
    f"        public I{modelName}Repository {modelName}s {{ get; }}\n\n"
    f"        public UnitOfWork({projectName}DbContext context)\n"
    f"        {{\n"
    f"            _context = context;\n\n"
    f"            Users = new UserRepository(_context);\n"
    f"            {modelName}s = new {modelName}Repository(_context);\n"
    f"        }}\n\n"
    f"        public IRepository<T> Repository<T>()\n"
    f"            where T : class\n"
    f"        {{\n"
    f"            if (typeof(T) == typeof(User))\n"
    f"            {{\n"
    f"                return Users as IRepository<T>;\n"
    f"            }}\n"
    f"            else if (typeof(T) == typeof({modelName}))\n"
    f"            {{\n"
    f"                return {modelName}s as IRepository<T>;\n"
    f"            }}\n"
    f"            return null;\n"
    f"        }}\n\n"
    f"        public int ExecuteSqlCommand(FormattableString _sql)\n"
    f"        {{\n"
    f"            return _context.Database.ExecuteSqlInterpolated(_sql);\n"
    f"        }}\n"
    f"        public async Task<int> ExecuteSqlCommandAsync(FormattableString _sql)\n"
    f"        {{\n"
    f"            return await _context.Database.ExecuteSqlInterpolatedAsync(_sql);\n"
    f"        }}\n"
    f"        public int ExecuteSqlCommand(string sql)\n"
    f"        {{\n"
    f"            using (var cmd = _context.Database.GetDbConnection().CreateCommand())\n"
    f"            {{\n"
    f"                cmd.CommandText = sql;\n"
    f"                if (cmd.Connection.State != ConnectionState.Open)\n"
    f"                    cmd.Connection.Open();\n"
    f"                return cmd.ExecuteNonQuery();\n\n"
    f"            }}\n"
    f"        }}\n"
    f"        public async Task<int> ExecuteSqlCommandAsync(string sql)\n"
    f"        {{\n"
    f"            using (var cmd = _context.Database.GetDbConnection().CreateCommand())\n"
    f"            {{\n"
    f"                cmd.CommandText = sql;\n"
    f"                if (cmd.Connection.State != ConnectionState.Open)\n"
    f"                    cmd.Connection.Open();\n"
    f"                return await cmd.ExecuteNonQueryAsync();\n\n"
    f"            }}\n"
    f"        }}\n\n"
    f"        public IDbContextTransaction BeginTransaction()\n"
    f"        {{\n"
    f"            return _context.Database.BeginTransaction();\n"
    f"        }}\n\n"
    f"        public IEnumerable<dynamic> GetObjectsToSQL(string sql)\n"
    f"        {{\n"
    f"            var resultSQLRequest = new List<dynamic>();\n"
    f"            using (var cmd = _context.Database.GetDbConnection().CreateCommand())\n"
    f"            {{\n"
    f"                cmd.CommandText = sql;\n"
    f"                if (cmd.Connection.State != ConnectionState.Open)\n"
    f"                    cmd.Connection.Open();\n\n"
    f"                using (var dataReader = cmd.ExecuteReader())\n"
    f"                {{\n\n"
    f"                    while (dataReader.Read())\n"
    f"                    {{\n"
    f"                        var dataRow = GetDataRow(dataReader);\n"
    f"                        resultSQLRequest.Add(dataRow);\n"
    f"                    }}\n"
    f"                }}\n"
    f"            }}\n"
    f"            return resultSQLRequest;\n"
    f"        }}\n"
    f"        public async Task<IEnumerable<dynamic>> GetObjectsToSQLAsync(string sql)\n"
    f"        {{\n"
    f"            var resultSQLRequest = new List<dynamic>();\n"
    f"            using (var cmd = _context.Database.GetDbConnection().CreateCommand())\n"
    f"            {{\n"
    f"                cmd.CommandText = sql;\n"
    f"                if (cmd.Connection.State != ConnectionState.Open)\n"
    f"                    cmd.Connection.Open();\n\n"
    f"                using (var dataReader = await cmd.ExecuteReaderAsync())\n"
    f"                {{\n\n"
    f"                    while (dataReader.Read())\n"
    f"                    {{\n"
    f"                        var dataRow = GetDataRow(dataReader);\n"
    f"                        resultSQLRequest.Add(dataRow);\n"
    f"                    }}\n"
    f"                }}\n"
    f"            }}\n"
    f"            return resultSQLRequest;\n"
    f"        }}\n"
    f"        private static dynamic GetDataRow(DbDataReader dataReader)\n"
    f"        {{\n"
    f"            var dataRow = new ExpandoObject() as IDictionary<string, object>;\n"
    f"            for (var fieldCount = 0; fieldCount < dataReader.FieldCount; fieldCount++)\n"
    f"                dataRow.Add(dataReader.GetName(fieldCount), dataReader[fieldCount]);\n"
    f"            return dataRow;\n"
    f"        }}\n\n"
    f"        public int Complete()\n"
    f"        {{\n"
    f"            return _context.SaveChanges();\n"
    f"        }}\n\n"
    f"        public async Task<int> CompleteAsync()\n"
    f"        {{\n"
    f"            return await _context.SaveChangesAsync();\n"
    f"        }}\n"
    f"        public void Dispose()\n"
    f"        {{\n"
    f"            _context.Dispose();\n"
    f"        }}\n"
    f"    }}\n"
    f"}}\n"
)

DBContextContent = (
    f"using Microsoft.EntityFrameworkCore;\n"
    f"using NetTopologySuite.Geometries;\n"
    f"using Newtonsoft.Json;\n"
    f"using {projectName}.Core.Entities;\n"
    f"using System;\n\n"
    f"namespace {projectName}.DAL\n"
    f"{{\n"
    f"    public class {projectName}DbContext : DbContext\n"
    f"    {{\n"
    f"        public {projectName}DbContext(DbContextOptions<{projectName}DbContext> options) : base(options)\n"
    f"        {{\n\n"
    f"        }}\n\n"
    f"		  public DbSet<{modelName}> {modelName}s {{ get; set; }}\n\n"
    f"        protected override void OnModelCreating(ModelBuilder modelBuilder)\n"
    f"        {{\n"
    f"            base.OnModelCreating(modelBuilder);\n"
    f"        }}\n"
    f"        protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)\n"
    f"        {{\n"
    f"            optionsBuilder.LogTo(System.Console.WriteLine);\n"
    f"        }}\n"
    f"    }}\n"
    f"}}\n"
)


def yesNoDialog(question, default_answer="yes"):
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
    fileExist = os.path.isfile(f"{currentPath}/{name}")

    if not folderExist:
        # Создать папку {currentDir+path}
        os.makedirs(currentPath)
        print(f"{Colors.OKGREEN}{path} директория создана!{Colors.ENDC}")

    if not fileExist:
        # Создать файл и записать содержимое
        with open(f"{currentPath}/{name}", "w") as file:
            file.write(content)
        print(f"{Colors.OKGREEN}Файл {name} создан!{Colors.ENDC}")
    else:
        print(f"{Colors.FAIL}Файл {name} существует{Colors.ENDC}")


def createFiles():
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
        f"Dto{modelName}.cs",
        dtoContent
    )
    createFile(
        f"/{projectName}.Core/RepositoryInterfaces",
        f"I{modelName}Repository.cs",
        iRepoContent
    )
    createFile(
        f"/{projectName}.Core/ServiceInterfaces",
        f"I{modelName}Service.cs",
        iServiceContent
    )
    createFile(
        f"/{projectName}.DAL/Repositories",
        f"{modelName}Repository.cs",
        repoContent
    )


def declarationFile(path, content, *changes):
    currentPath = currentDir + path
    fileExist = os.path.isfile(currentPath)

    if fileExist:
        for change in changes:
            putInFile(path, change.whereChange, change.whatChange)

    else:
        createFileAnswer = yesNoDialog(
            f"{Colors.OKCYAN}Файл {Colors.ENDC}{path} {Colors.OKCYAN}не найден. Создать его?{Colors.ENDC}", "no")
        if createFileAnswer:
            filePath = Path(path)
            createFile(filePath.parent, filePath.name, content)
        return


def declarationFiles():
    # MapProfile.cs
    declarationFile(
        f"/{projectName}.Api/AutoMapper/MapProfile.cs",
        mapProfileContent,
        ChangeParams(
            "Configure",
            f"\tConfigure{modelName}();"
        ),
        ChangeParams(
            "private void Configure",
            (
                f"private void Configure{modelName}()\n"
                f"\t\t{{\n"
                f"\t\t    CreateMap<{modelName}, Dto{modelName}>();\n"
                f"\t\t    CreateMap<Dto{modelName}, {modelName}>();\n"
                f"\t\t}}"
            )
        )
    )
    # Startup.cs
    declarationFile(
        f"/{projectName}.Api/Startup.cs",
        startupContent,
        ChangeParams(
            "services.AddScoped<I",
            f"\tservices.AddScoped<I{modelName}Service>(provider =>\n"
            f"\t\t\t\tnew {modelName}Service(provider.GetService<IUnitOfWork>()));\n"
        )
    )
    # IUnitOfWork
    declarationFile(
        f"/{projectName}.Core/RepositoryInterfaces/IUnitOfWork.cs",
        iUnitOfWorkContent,
        ChangeParams(
            "{ get; }",
            f"I{modelName}Repository {modelName}s {{ get; }}"
        )
    )
    # UnitOfWork.cs
    declarationFile(
        f"/{projectName}.DAL/UnitOfWork.cs",
        unitOfWorkContent,
        ChangeParams(
            "{ get; }",
            f"public I{modelName}Repository {modelName}s {{ get; }}"
        ),
        ChangeParams(
            "(_context);",
            f"\t{modelName}s = new {modelName}Repository(_context);"
        ),
        ChangeParams(
            "else if (typeof(T) == typeof(",
            f"\telse if (typeof(T) == typeof({modelName}))\n"
            f"\t\t\t{{\n"
            f"\t\t\t\treturn {modelName}s as IRepository<T>;\n"
            f"\t\t\t}}"
        )
    )
    # DBContext.cs
    declarationFile(
        f"/{projectName}.DAL/{projectName}DBContext.cs",
        DBContextContent,
        ChangeParams(
            "public DbSet",
            f"public DbSet<{modelName}> {modelName}s {{ get; set; }}"
        )
    )


def putInFile(path, replaceBefore, replaceString):
    path = currentDir + path
    with open(path, "r") as fileForRead, open(path, "r") as fileAsArray:
        # Считать данные из файла как строку
        fileData = fileForRead.read()

        # Считать данные из файла в массив
        lines = fileAsArray.readlines()

        # Проверяем, есть ли уже такая строка в файле (если мультистрок, то проверяет первую строку)
        print(
            f"\n{Colors.WARNING}Начинаем поиск в файле {Colors.ENDC}{path}\n")
        matchesInFile = indexContainingSubstring(
            lines, replaceString.split("\n")[0].strip())
        whereReplace = indexContainingSubstring(
            lines, replaceBefore)

        if matchesInFile == -1:
            # Существующая декларация не найдена
            if whereReplace == -1:
                # Не нашел где менять
                print("Не знаю, куда добавить\n")
            else:
                # Нашел где менять
                print("Нашел куда добавить, сейчас сделаю!" + "\n")
                replacedData = fileData.replace(
                    lines[whereReplace],
                    f"\t\t{replaceString}\n{lines[whereReplace]}"
                )
                with open(path, "w") as fileForWrite:
                    fileForWrite.write(replacedData)
                print(
                    f"{Colors.OKGREEN}Декларация прошла успешно!{Colors.ENDC}\n")
        else:
            # Существующая декларация найдена
            print(
                f"В файле: {path} {Colors.FAIL}Уже имеется{Colors.ENDC} строка:\n{replaceString}\n{Colors.FAIL}не меняю!{Colors.ENDC}\n")
            return


def indexContainingSubstring(theList, substring):
    for i, s in enumerate(theList):
        if substring in s:
            return i
    return -1


def main():
    createFolderAndDeclareAsk = yesNoDialog(
        f"\nБудут созданы следующие файлы:\n"
        f"{Colors.WARNING}/{projectName}.Api/Controllers/{modelName}Controller.cs\n"
        f"/{projectName}.BLL/Services/{modelName}Service.cs\n"
        f"/{projectName}.Core/Models/Dto/{modelName}/Dto{modelName}.cs\n"
        f"/{projectName}.Core/RepositoryInterfaces/I{modelName}Repository.cs\n"
        f"/{projectName}.Core/ServiceInterfaces/I{modelName}Service.cs\n"
        f"/{projectName}.DAL/Repositories/{modelName}Repository.cs{Colors.ENDC}\n\n"
        f"Произведены декларации в следующих файлах:\n"
        f"{Colors.WARNING}/{projectName}.Api/AutoMapper/MapProfile.cs{Colors.ENDC}\n"
        f"\t{Colors.HEADER}Configure{modelName}();\n"
        f"\tprivate void Configure{modelName}()\n"
        f"\t{{\n"
        f"\t\tCreateMap<{modelName}, Dto{modelName}>();\n"
        f"\t\tCreateMap<Dto{modelName}, {modelName}>();\n"
        f"\t}}{Colors.ENDC}\n\n"
        f"{Colors.WARNING}/{projectName}.Api/Startup.cs{Colors.ENDC}\n"
        f"\t{Colors.HEADER}services.AddScoped<{modelName}Service>(provider =>\n"
        f"\tnew {modelName}Service(provider.GetService<IUnitOfWork>()));{Colors.ENDC}\n\n"
        f"{Colors.WARNING}/{projectName}.Core/RepositoryInterfaces/IUnitOfWork.cs{Colors.ENDC}\n"
        f"\t{Colors.HEADER}I{modelName}Repository {modelName}s {{ get; }}{Colors.ENDC}\n\n"
        f"{Colors.WARNING}/{projectName}.DAL/UnitOfWork.cs{Colors.ENDC}\n"
        f"\t{Colors.HEADER}public I{modelName}Repository {modelName}s {{ get; }}\n"
        f"\t{modelName}s = new {modelName}Repository(_context);\n"
        f"\telse if (typeof(T) == typeof({modelName}))\n"
        f"\t{{\n"
        f"\t\treturn {modelName}s as IRepository<T>;\n"
        f"\t}}{Colors.ENDC}\n\n"
        f"{Colors.WARNING}/{projectName}.DAL/{projectName}DBContext.cs{Colors.ENDC}\n"
        f"\t{Colors.HEADER}public DbSet<{modelName}> {modelName}s {{ get; set; }}{Colors.ENDC}\n\n"
        f"Вы подтверждаете создание данных файлов и описанные декларации?", "no")

    if createFolderAndDeclareAsk:
        createFiles()
        declarationFiles()
    else:
        print(f"{Colors.OKGREEN}Понял, выключаюсь!{Colors.ENDC}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
