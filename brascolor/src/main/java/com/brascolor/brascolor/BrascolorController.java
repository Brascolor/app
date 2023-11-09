package com.brascolor.brascolor;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.RequestMapping;
//import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.SessionAttributes;
//import org.springframework.web.bind.annotation.ResponseBody;
//import org.springframework.web.bind.annotation.RestController;
import org.springframework.beans.factory.annotation.Autowired;


@Controller
@SessionAttributes(value = {"user", "func"})
public class BrascolorController {

    @Autowired
    private JdbcTemplate jdbcTemplate;

    @ModelAttribute("user")
    public User getUser() {
        return new User();
    }
    
    @GetMapping("/login")
    public String login(@ModelAttribute("user") User user){
        if(user.isLoggedIn()){
            return "redirect:/"; 
        }
        return "components/login";
    }

    @PostMapping("/login")
    //Map<String, Object> - param func = new HashMap<>(); - tudo fica na funcao
    //List<Map<String, Object>> func = jdbcTemplate.queryForList("SELECT * FROM funcionario WHERE idFunc = ? AND senha = ?", username, pwd); - para pegar os dados
    //model.addAttribute("func", func); - para enviar os dados
    //response.put("func", func); - para enviar os dados
    //return response
    public String login(@RequestParam("idFunc") String username, @RequestParam("password") String pwd, @ModelAttribute("user") User user){
        if(user.isLoggedIn()){
            return "redirect:/"; 
        }
        if(username.equals("123456") && pwd.equals("jefferson")){
            user.setLoggedIn(true);
            return "redirect:/"; 
        }
        return "components/login";
    }

    @PostMapping("/logout")
    public String logout(@ModelAttribute("user") User user){
        user.setLoggedIn(false);
        return "redirect:/login";
    }

    @GetMapping("/logout")
    public String logout(){
        return "components/login";
    }

    @GetMapping("/")
    public String home() { 
        return "components/home";
    }

    // @PostMapping("/os")
    // public String os(){
        
    // }

    // @GetMapping("/os")
    // public String os() { 
    //     return "components/os";
    // }
}
