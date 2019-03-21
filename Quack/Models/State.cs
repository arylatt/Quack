using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using System.ComponentModel.DataAnnotations;

namespace Quack.Models
{
    public class State
    {
        [Required]
        public bool Enabled { get; set; }
    }
}
