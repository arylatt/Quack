using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Quack.Models;

namespace Quack.Controllers
{
    [Produces("application/json")]
    [Route("api/quack")]
    [ApiController]
    public class QuackController : ControllerBase
    {
        /// <summary>
        /// Quack
        /// </summary>
        [HttpPut]
        public ActionResult Put()
        {
            // Trigger the duck
            return NoContent();
        }
    }
}
