using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Quack.Models;

namespace Quack.Controllers
{
    [Produces("application/json")]
    [Route("api/state")]
    [ApiController]
    public class StateController : ControllerBase
    {
        /// <summary>
        /// To Quack, or not to Quack? This is the answer...
        /// </summary>
        [HttpGet]
        public ActionResult<State> Get()
        {
            // Get the state and return it
            return new State { Enabled = false };
        }

        /// <summary>
        /// To Quack, or not to Quack? That is the question...
        /// </summary>
        [HttpPut]
        public ActionResult Put([FromBody] State state)
        {
            // Update state storage to reflect change
            return NoContent();
        }
    }
}
